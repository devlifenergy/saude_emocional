# teste_conexao.py
import streamlit as st
import gspread
from datetime import datetime

# 1. AUTENTICAÇÃO
# O nome da seção [google_credentials] deve ser o mesmo que você usou no secrets.toml
st.title("Teste de Conexão com Google Sheets")

try:
    # Cria uma cópia editável das credenciais
    creds_dict = dict(st.secrets["google_credentials"])
    # Corrige a formatação da chave privada
    creds_dict['private_key'] = creds_dict['private_key'].replace('\\n', '\n')
    
    # Autentica no Google
    gc = gspread.service_account_from_dict(creds_dict)
    
    # Abre a planilha pelo nome exato
    spreadsheet = gc.open("Teste Conexão Streamlit")
    
    # Seleciona a primeira aba
    worksheet = spreadsheet.sheet1
    
    st.success("Conexão com Google Sheets bem-sucedida!")

except Exception as e:
    st.error(f"Erro ao conectar com o Google Sheets: {e}")
    st.stop()


# 2. FORMULÁRIO SIMPLES
with st.form("meu_formulario"):
    nome = st.text_input("Nome")
    mensagem = st.text_area("Mensagem")
    submitted = st.form_submit_button("Enviar para Planilha")

# 3. LÓGICA DE ENVIO
if submitted:
    if not nome or not mensagem:
        st.warning("Por favor, preencha todos os campos.")
    else:
        with st.spinner("Enviando dados..."):
            try:
                # Cria a linha a ser adicionada
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                new_row = [timestamp, nome, mensagem]
                
                # Adiciona a nova linha à planilha
                worksheet.append_row(new_row, value_input_option='USER_ENTERED')
                
                st.success("Dados enviados com sucesso para a planilha!")
                st.balloons()
            except Exception as e:
                st.error(f"Erro ao enviar dados para a planilha: {e}")