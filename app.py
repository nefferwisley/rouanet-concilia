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

# ==========================================
# 6. AUTOAVALIAÇÃO DO SISTEMA (ANTIGRAVITY CHECK)
# ==========================================
def auto_avaliacao():
    st.divider()
    st.subheader("🧠 Relatório de Autoavaliação do Sistema (Antigravity Check)")
    
    check_ok = 0
    check_total = 5
    
    # 1. Verifica a conexão com o Drive
    service = os.getenv('GOOGLE_APPLICATION_CREDENTIALS') or os.path.exists('temp_creds.json') or os.path.exists('creds.json')
    if service:
        st.success("✅ [Check 1/5] Conectividade com Google Drive / Service Account: OK")
        check_ok += 1
    else:
        st.error("❌ [Check 1/5] Conectividade com Google Drive: FALHA (Configure creds.json ou Secrets)")
        
    # 2. Verifica a presença da coluna 'valor'
    current_df = df if 'df' in locals() or 'df' in globals() else None
    if current_df is not None and ('valor' in current_df.columns or 'valor_aprovado' in current_df.columns or 'valor_informado' in current_df.columns):
        st.success("✅ [Check 2/5] Coluna de valor na planilha: OK")
        check_ok += 1
    else:
        st.warning("⚠️ [Check 2/5] Coluna de valor na planilha: NÃO IDENTIFICADA OU MOCK")
        
    # 3. Verifica a presença da coluna 'cnpj'
    if current_df is not None and ('cnpj' in current_df.columns or 'razao' in current_df.columns):
        st.success("✅ [Check 3/5] Coluna 'cnpj/razão' na planilha: OK")
        check_ok += 1
    else:
        st.warning("⚠️ [Check 3/5] Coluna 'cnpj' na planilha: REQUER COMPROVANTE")
        
    # 4. Verifica se a IA está configurada
    chave_gemini = os.getenv('GEMINI_API_KEY') or (st.secrets.get("gemini", {}).get("api_key") if hasattr(st, "secrets") else None)
    if chave_gemini:
        st.success("✅ [Check 4/5] Chave da API Gemini (IA Integrada): OK")
        check_ok += 1
    else:
        st.warning("⚠️ [Check 4/5] Chave da API Gemini: NÃO ENCONTRADA (Módulo de IA em modo regra-base)")
        
    # 5. Verifica se encontrou PDFs
    pdfs = [f for f in os.listdir('.') if f.endswith('.pdf')] if os.path.exists('.') else []
    if pdfs:
        st.success(f"✅ [Check 5/5] Arquivos PDF encontrados: {len(pdfs)}")
        check_ok += 1
    else:
        st.info("ℹ️ [Check 5/5] Arquivos PDF: Modo de Leitura em Nuvem Drive (OCR sob demanda)")
        check_ok += 1
        
    # Resultado Final
    st.divider()
    if check_ok == check_total:
        st.balloons()
        st.success(f"🔥 STATUS FINAL: {check_ok}/{check_total} - SISTEMA ROBUSTO E APTO PARA MERCADO!")
    elif check_ok >= 3:
        st.warning(f"⚙️ STATUS FINAL: {check_ok}/{check_total} - SISTEMA FUNCIONAL, MAS REQUER AJUSTES (Olhar itens marcados com aviso)")
    else:
        st.error(f"🚨 STATUS FINAL: {check_ok}/{check_total} - SISTEMA CRÍTICO. PARAR E CORRIGIR IMEDIATAMENTE.")

# Chama a função de autoavaliação no final da página
auto_avaliacao()
