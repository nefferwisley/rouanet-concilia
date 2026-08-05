import streamlit as st
import pandas as pd
import io
import os
import json

try:
    import gdown
    HAS_GDOWN = True
except ImportError:
    HAS_GDOWN = False

# 1. Configuração inicial da página
st.set_page_config(page_title="Painel Offline - Drive", layout="wide", page_icon="📁")
st.title("📁 Projeto 1961 - Leitura Exclusiva do Drive")
st.caption("🎬 Produzido por: **Circunstância Cinematográfica Ltda** | 👤 Controller Responsável: **Júlia Sousa**")

# PASSO 1: Configure o ID da sua pasta do Drive (Padrão: 1. Pagamentos do Projeto 1961)
DEFAULT_1961_PASTA_ID = "1ydDeUQQzcTRk6QhJY_QIow1SfaJyL0Mj"
DEFAULT_1961_PLANILHA_ID = "1q52xZirlzYCqpQJ7ldYNG9wQrVodPuJc"

PASTA_DRIVE_ID = st.sidebar.text_input(
    "ID da Pasta do Google Drive (PASTA_DRIVE_ID):",
    value=os.getenv("PASTA_DRIVE_ID", DEFAULT_1961_PASTA_ID),
    help="ID da pasta do Drive contendo os comprovantes e a planilha 2. Conciliação 1961.xlsx"
)

# PASSO 2: Função para ler um arquivo do Drive usando o token do robô
def ler_arquivo_do_drive(nome_arquivo, pasta_id):
    if not pasta_id or pasta_id == "COLE_AQUI_O_ID_DA_SUA_PASTA":
        return None
    if not HAS_GDOWN:
        st.error("A biblioteca 'gdown' não está instalada. Execute `pip install gdown`.")
        return None
    try:
        # O gdown procura o arquivo dentro da pasta especificada pelo ID
        # O formato é: https://drive.google.com/uc?export=download&id=ID_DO_ARQUIVO
        url_pasta = f"https://drive.google.com/drive/folders/{pasta_id}"
        
        # Lista os arquivos dentro da pasta
        arquivos = gdown.list_folder(url_pasta, quiet=True)
        
        if arquivos:
            for arquivo in arquivos:
                if arquivo.get('name') == nome_arquivo:
                    # Baixa o conteúdo do arquivo para a memória (sem salvar no disco do servidor)
                    return gdown.download(f"https://drive.google.com/uc?id={arquivo['id']}", output=None, quiet=True)
        return None
    except Exception as e:
        st.error(f"Erro ao ler do Drive: {e}")
        return None

# PASSO 3: Configurar a autenticação do "Robô" (Service Account)
# No Streamlit Cloud, você vai colocar o conteúdo do seu JSON nos "Secrets"
# No seu computador local, você coloca o JSON na mesma pasta do arquivo
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

    # Se não rodar na nuvem, tenta ler um arquivo local chamado 'creds.json'
    if os.path.exists('creds.json'):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'creds.json'
        return True
    else:
        st.warning("Nenhuma credencial do Drive encontrada. Configure a Service Account.")
        return False

# Executa a autenticação
configurar_autenticacao()

# PASSO 4: Interface do usuário
st.write("Este painel está puxando os dados da pasta do Google Drive.")

# Tenta carregar a planilha
st.subheader("📋 Carregando Planilha...")
planilha_bytes = ler_arquivo_do_drive("planilha_projeto.csv", PASTA_DRIVE_ID)

if planilha_bytes:
    try:
        df = pd.read_csv(io.BytesIO(planilha_bytes))
        st.success("✅ Planilha CSV carregada do Drive!")
        st.dataframe(df, use_container_width=True)
        
        # Simula a leitura dos PDFs (para teste)
        st.subheader("📎 Comprovantes no Drive")
        st.info("O sistema encontrou a planilha. O próximo passo (Sprint 2) será ler os PDFs da mesma pasta e comparar os valores usando OCR.")
        
    except Exception as e:
        st.error(f"Erro ao ler o arquivo CSV: {e}")
else:
    st.warning("⚠️ Nenhum arquivo chamado 'planilha_projeto.csv' encontrado na pasta do Drive.")
    st.write("Verifique se o ID da pasta está correto e se a pasta está compartilhada com o e-mail do robô.")
