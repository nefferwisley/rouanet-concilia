import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="RouanetConcilia", layout="wide")
st.title("🎭 Painel de Prestação de Contas (Nuvem)")

st.write("Este painel está puxando os dados da API do SALIC (MinC).")

@st.cache_data(ttl=600)
def buscar_api_salic():
    try:
        # ATENÇÃO: Substitua essa URL pelo endereço correto da API que você tem
        url = "https://api.salic.cultura.gov.br/v1/projetos?limit=10"
        resposta = requests.get(url)
        if resposta.status_code == 200:
            dados = resposta.json()
            # Simulação: transformando os dados em tabela
            return pd.DataFrame(dados['_embedded']['projetos'])
        else:
            return None
    except Exception as e:
        return None

# Tenta carregar os dados
df = buscar_api_salic()

if df is not None and not df.empty:
    st.success("✅ Dados carregados da API com sucesso!")
    st.dataframe(df, use_container_width=True)
    
    # Simulação de menu para evoluir depois
    opcao = st.radio("Escolha uma ação:", ["Ver Tudo", "Ver Pendências"])
    if opcao == "Ver Pendências":
        st.info("Aqui no futuro vamos filtrar apenas os erros.")
else:
    st.error("❌ Não foi possível conectar à API do SALIC. O sistema está no modo offline.")
    st.write("**Para testar na nuvem:** Como a API do governo é instável, o sistema está mostrando um exemplo fictício para você ver o painel funcionando.")
    
    # Dados de exemplo para o painel nunca ficar vazio
    dados_exemplo = {
        "ID": [1, 2, 3],
        "Projeto": ["Projeto A", "Projeto B", "Projeto C"],
        "Valor Aprovado": [1000.00, 2500.00, 3500.00],
        "Status": ["Aprovado", "Pendente", "Aprovado"]
    }
    df_exemplo = pd.DataFrame(dados_exemplo)
    st.dataframe(df_exemplo, use_container_width=True)