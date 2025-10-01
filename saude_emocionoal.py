# app_lifenergy_esg_nr1_google_sheets_v2.py
import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from gspread_dataframe import set_with_dataframe

# --- PALETA DE CORES E CONFIGURAÇÃO DA PÁGINA ---
# (O CSS e a configuração da página permanecem os mesmos)
COLOR_PRIMARY = "#70D1C6"
COLOR_TEXT_DARK = "#333333"
COLOR_BACKGROUND = "#FFFFFF"
st.set_page_config(page_title="Formulário Lifenergy - ESG & NR‑1", layout="wide")
# O CSS foi omitido aqui para economizar espaço, mas deve estar no seu script
st.markdown(f"""<style>...</style>""", unsafe_allow_html=True) 

# --- CONEXÃO COM GOOGLE SHEETS (COM CORREÇÃO) ---
try:
    # Pega as credenciais do Streamlit Secrets
    creds_dict = st.secrets["gcp_service_account"]
    
    # ##### CORREÇÃO APLICADA AQUI #####
    # Corrige a formatação da chave privada que causa o erro
    creds_dict['private_key'] = creds_dict['private_key'].replace('\\n', '\n')
    
    # Autentica usando o dicionário de credenciais corrigido
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

        # --- LÓGICA DE CÁLCULO (Permanece a mesma) ---
        # (O código de cálculo foi omitido aqui para economizar espaço)
        # ...
        # ...
        
        # --- NOVA LÓGICA DE EXPORTAÇÃO PARA GOOGLE SHEETS ---
        with st.spinner("Enviando dados para a planilha..."):
            
            # 1. Preparar dados das respostas (formato longo)
            timestamp_str = datetime.now().isoformat(timespec="seconds")
            respostas_para_enviar = []
            # (O código para preparar as respostas para enviar foi omitido aqui, mas permanece o mesmo)
            # ...
            
            df_respostas_gs = pd.DataFrame(respostas_para_enviar)
            
            # Adiciona as novas linhas à planilha, sem o cabeçalho
            ws_respostas.append_rows(df_respostas_gs.values.tolist(), value_input_option='USER_ENTERED')

            # 2. Preparar dados de observações
            if observacoes:
                # (O código para preparar as observações foi omitido aqui, mas permanece o mesmo)
                # ...
                df_obs_gs = pd.DataFrame(dados_obs)
                ws_observacoes.append_rows(df_obs_gs.values.tolist(), value_input_option='USER_ENTERED')
        
        st.success("Suas respostas foram enviadas com sucesso para a planilha central!")
        st.info("Você já pode fechar esta janela.")