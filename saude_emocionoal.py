# app_lifenergy_esg_nr1_final.py
import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from gspread_dataframe import set_with_dataframe
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# --- PALETA DE CORES E CONFIGURAÇÃO DA PÁGINA ---
COLOR_PRIMARY = "#70D1C6"
COLOR_TEXT_DARK = "#333333"
COLOR_BACKGROUND = "#FFFFFF"

st.set_page_config(
    page_title="Formulário Lifenergy - ESG & NR‑1",
    layout="wide"
)

# --- CSS CUSTOMIZADO PARA A INTERFACE ---
# (O CSS foi omitido aqui para economizar espaço, mas deve estar no seu script)
st.markdown(f"""<style>...</style>""", unsafe_allow_html=True) 

# --- CONEXÃO COM GOOGLE SHEETS (VERSÃO CORRIGIDA) ---
try:
    # Pega as credenciais do Streamlit Secrets (que são somente leitura)
    creds_from_secrets = st.secrets["gcp_service_account"]
    
    # ##### CORREÇÃO APLICADA AQUI #####
    # 1. Cria uma CÓPIA editável do dicionário de credenciais
    creds_dict = dict(creds_from_secrets)
    
    # 2. Corrige a formatação da chave privada na CÓPIA
    creds_dict['private_key'] = creds_dict['private_key'].replace('\\n', '\n')
    
    # 3. Autentica usando a cópia corrigida
    gc = gspread.service_account_from_dict(creds_dict)
    
    # Abre a planilha pelo nome que você deu a ela
    spreadsheet = gc.open("Respostas App Lifenergy")
    # Seleciona as abas
    ws_respostas = spreadsheet.worksheet("Respostas")
    ws_observacoes = spreadsheet.worksheet("Observacoes")
except Exception as e:
    st.error(f"Erro ao conectar com o Google Sheets: {e}")
    st.info("Verifique se as credenciais no Secrets estão corretas e se a planilha foi compartilhada com o 'client_email'.")
    st.stop()


# --- CABEÇALHO, IDENTIFICAÇÃO, INSTRUÇÕES E LÓGICA DO QUESTIONÁRIO ---
# (Todo o código da interface do usuário até o botão de finalizar permanece o mesmo)
# O código foi omitido aqui para economizar espaço, mas deve estar no seu script
# ...
# ...
# ...

# --- BOTÃO DE FINALIZAR E LÓGICA DE RESULTADOS/EXPORTAÇÃO ---
if st.button("Finalizar e Enviar Respostas", type="primary"):
    if not st.session_state.respostas:
        st.warning("Nenhuma resposta foi preenchida.")
    else:
        st.subheader("Enviando e Processando Resultados...")
        
        # Lógica de cálculo (permanece a mesma)
        # ...
        
        with st.spinner("Enviando dados para a planilha..."):
            
            # 1. Preparar dados das respostas
            timestamp_str = datetime.now().isoformat(timespec="seconds")
            respostas_para_enviar = []
            # ... (código para preparar as respostas para enviar permanece o mesmo)
            
            df_respostas_gs = pd.DataFrame(respostas_para_enviar)
            ws_respostas.append_rows(df_respostas_gs.values.tolist(), value_input_option='USER_ENTERED')

            # 2. Preparar dados de observações
            if observacoes:
                # ... (código para preparar as observações permanece o mesmo)
                df_obs_gs = pd.DataFrame(dados_obs)
                ws_observacoes.append_rows(df_obs_gs.values.tolist(), value_input_option='USER_ENTERED')
        
        st.success("Suas respostas foram enviadas com sucesso para a planilha central!")
        st.info("Você já pode fechar esta janela.")