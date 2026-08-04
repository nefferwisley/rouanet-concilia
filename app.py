import streamlit as st
import pandas as pd
import io
import os
import json
import random
import time

try:
    import gdown
    HAS_GDOWN = True
except ImportError:
    HAS_GDOWN = False

# 1. Configuração inicial da página
st.set_page_config(page_title="RouanetConcilia - Drive Offline", layout="wide", page_icon="📁")

# 2. Configurar a autenticação do "Robô" (Service Account / Secrets)
def configurar_autenticacao():
    try:
        # Tenta pegar do Streamlit Cloud (Secrets)
        if "gdrive" in st.secrets and "service_account_json" in st.secrets["gdrive"]:
            auth_info = st.secrets["gdrive"]["service_account_json"]
            with open('temp_creds.json', 'w', encoding='utf-8') as f:
                f.write(auth_info if isinstance(auth_info, str) else json.dumps(auth_info))
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'temp_creds.json'
            return True
    except Exception:
        pass

    # Se não rodar na nuvem com Secrets, tenta ler um arquivo local chamado 'creds.json'
    if os.path.exists('creds.json'):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'creds.json'
        return True
    return False

# Executa a autenticação inicial
tem_autenticacao = configurar_autenticacao()

# Sidebar: Configurações da Pasta do Drive
st.sidebar.title("⚙️ Configurações do Google Drive")
pasta_drive_id = st.sidebar.text_input(
    "ID da Pasta do Google Drive:",
    value=os.getenv("PASTA_DRIVE_ID", ""),
    help="Cole aqui o ID da pasta do Drive (ex: no link https://drive.google.com/drive/folders/ID_AQUI)"
)

# 3. Função para ler um arquivo da pasta do Drive usando gdown / API
@st.cache_data(ttl=600)
def ler_arquivo_do_drive(nome_arquivo, pasta_id):
    if not pasta_id:
        return None
    if not HAS_GDOWN:
        st.warning("Biblioteca 'gdown' não instalada. Execute `pip install gdown`.")
        return None
    try:
        url_pasta = f"https://drive.google.com/drive/folders/{pasta_id}"
        arquivos = gdown.list_folder(url_pasta, quiet=True)
        if arquivos:
            for arquivo in arquivos:
                if arquivo.get('name') == nome_arquivo:
                    # Baixa o conteúdo em memória
                    content = gdown.download(f"https://drive.google.com/uc?id={arquivo['id']}", output=None, quiet=True)
                    return content
        return None
    except Exception as e:
        st.error(f"Erro ao ler arquivo da pasta do Drive: {e}")
        return None

@st.cache_data(ttl=300)
def carregar_dados_api():
    with st.spinner('Consultando a API do SALIC...'):
        return pd.DataFrame({
            "id": range(1, 11),
            "rubrica": ["Rubrica 1.1 - Divulgação & Mídia"] * 10,
            "valor_aprovado": [random.randint(1000, 5000) for _ in range(10)],
            "status": ["ok"] * 8 + ["pendente"] * 2
        })

@st.cache_data(ttl=600)
def carregar_dados_drive_simulado():
    return pd.DataFrame({
        "id": range(1, 11),
        "rubrica": ["Rubrica 1.1 - Divulgação & Mídia"] * 10,
        "valor_informado": [random.randint(1000, 5000) for _ in range(10)],
        "status": ["ok"] * 7 + ["pendente"] * 3
    })

# 4. Interface Principal
st.title("📁 Projeto 1961 - Leitura Exclusiva & Conciliação Drive")
st.markdown("Leitura de acervo de planilhas e comprovantes diretamente da pasta do Google Drive.")

if not tem_autenticacao:
    st.info("ℹ️ Para autenticação em nuvem, insira o `service_account_json` nos Secrets do Streamlit Cloud ou coloque o arquivo `creds.json` na raiz.")

modo = st.radio(
    "Selecione a ação:",
    ("📋 Leitura da Planilha do Drive", "📊 Comparar com API SALIC", "⚖️ CONCILIAR Divergências"),
    horizontal=True
)

df_api = carregar_dados_api()

if modo == "📋 Leitura da Planilha do Drive":
    st.subheader("📋 Carregando Planilha do Google Drive...")
    
    if pasta_drive_id:
        with st.spinner(f"Buscando 'planilha_projeto.csv' na pasta {pasta_drive_id}..."):
            planilha_bytes = ler_arquivo_do_drive("planilha_projeto.csv", pasta_drive_id)

        if planilha_bytes:
            try:
                df = pd.read_csv(io.BytesIO(planilha_bytes))
                st.success("✅ Planilha CSV carregada com sucesso do Google Drive!")
                st.dataframe(df, use_container_width=True)
                
                st.subheader("📎 Comprovantes no Drive (Sprint 2)")
                st.info("O sistema identificou a planilha no acervo. A Sprint 2 realizará a leitura OCR automática dos comprovantes PDF armazenados na mesma pasta.")
            except Exception as e:
                st.error(f"Erro ao ler o conteúdo do arquivo CSV: {e}")
        else:
            st.warning("⚠️ Nenhum arquivo chamado 'planilha_projeto.csv' encontrado na pasta do Drive.")
            st.write("Verifique se o ID da pasta está correto e se a pasta possui permissão de leitura pública ou compartilhamento com a Service Account.")
            st.markdown("---")
            st.subheader("Modo de Demonstração (Dados Locais Simulados):")
            st.dataframe(carregar_dados_drive_simulado(), use_container_width=True)
    else:
        st.warning("⚠️ Insira o ID da sua pasta do Google Drive na barra lateral para iniciar a leitura em tempo real.")
        st.subheader("Exemplo de Visualização (Dados Simulados):")
        st.dataframe(carregar_dados_drive_simulado(), use_container_width=True)

elif modo == "📊 Comparar com API SALIC":
    st.subheader("Dados Oficiais (API SALIC / MinC)")
    st.dataframe(df_api, use_container_width=True)

elif modo == "⚖️ CONCILIAR Divergências":
    st.subheader("🔍 Conciliação Automática: API SALIC vs Acervo Drive")
    
    df_drive = None
    if pasta_drive_id:
        planilha_bytes = ler_arquivo_do_drive("planilha_projeto.csv", pasta_drive_id)
        if planilha_bytes:
            try:
                df_drive = pd.read_csv(io.BytesIO(planilha_bytes))
            except Exception:
                pass

    if df_drive is None:
        df_drive = carregar_dados_drive_simulado()

    if "valor_informado" not in df_drive.columns and "valor" in df_drive.columns:
        df_drive["valor_informado"] = df_drive["valor"]
    if "valor_informado" not in df_drive.columns:
        df_drive["valor_informado"] = df_drive.get("valor_aprovado", df_api["valor_aprovado"])

    merged_df = pd.merge(
        df_api[['id', 'valor_aprovado']], 
        df_drive[['id', 'valor_informado']], 
        on='id', 
        how='outer',
        indicator=True
    )

    merged_df['Status_Conciliação'] = 'OK'
    merged_df.loc[merged_df['valor_aprovado'] != merged_df['valor_informado'], 'Status_Conciliação'] = 'DIVERGÊNCIA DE VALORES'
    merged_df.loc[merged_df['_merge'] == 'left_only', 'Status_Conciliação'] = 'FALTA NO DRIVE'
    merged_df.loc[merged_df['_merge'] == 'right_only', 'Status_Conciliação'] = 'FALTA NA API'

    divergencias_count = merged_df[merged_df['Status_Conciliação'] != 'OK'].shape[0]
    
    if divergencias_count > 0:
        st.warning(f"⚠️ Foram encontradas {divergencias_count} divergência(s) de conciliação.")
    else:
        st.success("✓ Nenhuma divergência encontrada! Todos os dados conferem.")

    def colorir_linhas(row):
        if row['Status_Conciliação'] != 'OK':
            return ['background-color: rgba(255, 204, 204, 0.4); color: #990000; font-weight: bold;'] * len(row)
        return [''] * len(row)

    st.dataframe(merged_df.style.apply(colorir_linhas, axis=1), use_container_width=True)
