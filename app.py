import streamlit as st
import pandas as pd
import time
import os
import random

# 1. Configuração inicial da página
st.set_page_config(page_title="RouanetConcilia", layout="wide", page_icon="🎭")

# 2. Funções de Carregamento (com cache mágico do Streamlit)
@st.cache_data(ttl=300) # ttl=300 significa que a API será reconsultada a cada 5 min
def carregar_dados_api():
    with st.spinner('Consultando a API do SALIC...'):
        # Simulação da chamada real à API SALIC / MinC
        return pd.DataFrame({
            "id": range(1, 11),
            "rubrica": ["Rubrica 1.1 - Divulgação & Mídia"] * 10,
            "valor_aprovado": [random.randint(1000, 5000) for _ in range(10)],
            "status": ["ok"] * 8 + ["pendente"] * 2
        })

@st.cache_data(ttl=600) # Cache um pouco maior para leitura de acervo/Drive
def carregar_dados_drive():
    with st.spinner('Lendo a pasta do Google Drive...'):
        # Simulação de leitura de acervo / extratos da pasta do Drive
        return pd.DataFrame({
            "id": range(1, 11),
            "rubrica": ["Rubrica 1.1 - Divulgação & Mídia"] * 10,
            "valor_informado": [random.randint(1000, 5000) for _ in range(10)],
            "status": ["ok"] * 7 + ["pendente"] * 3
        })

# 3. Painel de Controle do Usuário
st.title("🎭 RouanetConcilia - Painel de Comparação & Conciliação")
st.markdown("Sistema de Conciliação Financeira para Prestação de Contas Lei Rouanet / SALIC-MinC")

modo = st.radio(
    "Selecione o modo de visualização:",
    ("📊 Exibir Dados da API (SALIC)", "📁 Exibir Dados da Pasta/Drive", "⚖️ CONCILIAR e Ver Divergências"),
    horizontal=True
)

# Carrega os dados uma única vez com o cache do Streamlit
df_api = carregar_dados_api()
df_drive = carregar_dados_drive()

# 4. Renderização conforme o modo escolhido
if modo == "📊 Exibir Dados da API (SALIC)":
    st.subheader("Dados Oficiais (SALIC / MinC)")
    st.dataframe(df_api, use_container_width=True)

elif modo == "📁 Exibir Dados da Pasta/Drive":
    st.subheader("Dados do Seu Acervo (Pasta / Google Drive)")
    st.dataframe(df_drive, use_container_width=True)

elif modo == "⚖️ CONCILIAR e Ver Divergências":
    st.subheader("🔍 Comparação entre fontes (SALIC vs Acervo Drive)")
    
    # Concatena os dois dataframes baseado no ID
    merged_df = pd.merge(
        df_api[['id', 'valor_aprovado']], 
        df_drive[['id', 'valor_informado']], 
        on='id', 
        how='outer',
        indicator=True
    )

    # Cria colunas de status para facilitar a visualização
    merged_df['Status_Conciliação'] = 'OK'
    
    # Define regras de sinalização: 
    # DIVERGÊNCIA DE VALORES onde valor não bate (API vs Drive)
    # FALTA NO DRIVE ou FALTA NA API onde há ausência em um dos lados
    merged_df.loc[merged_df['valor_aprovado'] != merged_df['valor_informado'], 'Status_Conciliação'] = 'DIVERGÊNCIA DE VALORES'
    merged_df.loc[merged_df['_merge'] == 'left_only', 'Status_Conciliação'] = 'FALTA NO DRIVE'
    merged_df.loc[merged_df['_merge'] == 'right_only', 'Status_Conciliação'] = 'FALTA NA API'

    divergencias_count = merged_df[merged_df['Status_Conciliação'] != 'OK'].shape[0]
    
    if divergencias_count > 0:
        st.warning(f"⚠️ Foram encontradas {divergencias_count} divergência(s) de conciliação.")
    else:
        st.success("✓ Nenhuma divergência encontrada! Todos os dados conferem.")
    
    # Destaca com cores as linhas com inconsistência
    def colorir_linhas(row):
        if row['Status_Conciliação'] != 'OK':
            return ['background-color: rgba(255, 204, 204, 0.4); color: #990000; font-weight: bold;'] * len(row)
        return [''] * len(row)

    st.dataframe(merged_df.style.apply(colorir_linhas, axis=1), use_container_width=True)
