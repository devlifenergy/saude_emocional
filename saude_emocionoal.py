# app_saude_emocional_final.py
import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
import matplotlib.pyplot as plt

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

try:
    # Cria uma cópia editável das credenciais
    creds_dict = dict(st.secrets["google_credentials"])
    # Corrige a formatação da chave privada
    creds_dict['private_key'] = creds_dict['private_key'].replace('\\n', '\n')
    
    # Autentica no Google
    gc = gspread.service_account_from_dict(creds_dict)
    
    # Abre a planilha pelo nome exato
    spreadsheet = gc.open("Respostas Formularios")
    
    # Seleciona a primeira aba
    worksheet = spreadsheet.sheet1

except Exception as e:
    st.error(f"Erro ao conectar com o Google Sheets: {e}")
    st.stop()

# Seleciona as abas fora da função de cache
ws_respostas = spreadsheet.worksheet("Saude")


# --- CABEÇALHO DA APLICAÇÃO ---
col1, col2 = st.columns([1, 4])
with col1:
    try:
        st.image("logo_wedja.jpg", width=120)
    except FileNotFoundError:
        st.warning("Logo 'logo_wedja.jpg' não encontrada.")
with col2:
    st.markdown(f"""
    <div style="display: flex; flex-direction: column; justify-content: center; height: 100%;">
        <h2 style='color: {COLOR_TEXT_DARK}; margin: 0; padding: 0;'>Consultoria Lifenergy</h2>
        <p style='color: {COLOR_TEXT_DARK}; margin: 0; padding: 0;'>Cultura Organizacional com foco em Saúde Emocional</p>
    </div>
    """, unsafe_allow_html=True)


# --- SEÇÃO DE IDENTIFICAÇÃO ---
with st.container(border=True):
    st.markdown("<h3 style='text-align: center;'>Identificação Mínima</h3>", unsafe_allow_html=True)
    col1_form, col2_form = st.columns(2)
    with col1_form:
        respondente = st.text_input("Respondente:", key="input_respondente")
        data = st.text_input("Data:", datetime.now().strftime('%d/%m/%Y'))
    with col2_form:
        organizacao_coletora = st.text_input("Organização Coletora:", "Instituto Wedja de Socionomia", disabled=True)

# --- INSTRUÇÕES ---
with st.expander("Ver Orientações aos Respondentes", expanded=True):
    st.info(
        """
        - **Janela de referência:** últimos 3 meses.
        - **Escala Likert 1–5:** 1=Discordo totalmente • 2=Discordo • 3=Neutro • 4=Concordo • 5=Concordo totalmente.
        - **Confidencialidade/LGPD:** Dados agrupados para fins de diagnóstico; sem avaliações individuais.
        """
    )


# --- LÓGICA DO QUESTIONÁRIO (BACK-END) ---
@st.cache_data
def carregar_itens():
    # ##### ALTERAÇÃO APLICADA AQUI: CU -> CO #####
    data = [
        ('CO01', 'Cultura Organizacional', 'PRÁTICAS', 'As práticas diárias refletem o que a liderança diz e cobra.', 'NÃO'),
        ('CO02', 'Cultura Organizacional', 'PRÁTICAS', 'Processos críticos têm donos claros e rotina de revisão.', 'NÃO'),
        ('CO03', 'Cultura Organizacional', 'SÍMBOLOS', 'A comunicação visual (quadros, murais, campanhas) reforça os valores da empresa.', 'NÃO'),
        ('CO04', 'Cultura Organizacional', 'SÍMBOLOS', 'Reconhecimentos e premiações estão alinhados ao comportamento esperado.', 'NÃO'),
        ('CO05', 'Cultura Organizacional', 'HÁBITOS & COMPORTAMENTOS', 'Feedbacks e aprendizados com erros ocorrem sem punição inadequada.', 'NÃO'),
        ('CO06', 'Cultura Organizacional', 'HÁBITOS & COMPORTAMENTOS', 'Conflitos são tratados com respeito e foco em solução.', 'NÃO'),
        ('CO07', 'Cultura Organizacional', 'VALORES ÉTICOS & MORAIS', 'Integridade e respeito orientam decisões, mesmo sob pressão.', 'NÃO'),
        ('CO08', 'Cultura Organizacional', 'VALORES ÉTICOS & MORAIS', 'Não há tolerância a discriminação, assédio ou retaliação.', 'NÃO'),
        ('CO09', 'Cultura Organizacional', 'PRINCÍPIOS', 'Critérios de decisão são transparentes e consistentes.', 'NÃO'),
        ('CO10', 'Cultura Organizacional', 'PRINCÍPIOS', 'A empresa cumpre o que promete a pessoas e clientes.', 'NÃO'),
        ('CO11', 'Cultura Organizacional', 'CRENÇAS', 'Acreditamos que segurança e saúde emocional são inegociáveis.', 'NÃO'),
        ('CO12', 'Cultura Organizacional', 'CRENÇAS', 'Acreditamos que diversidade melhora resultados.', 'NÃO'),
        ('CO13', 'Cultura Organizacional', 'CERIMÔNIAS', 'Há rituais de reconhecimento (semanal/mensal) que celebram comportamentos-chave.', 'NÃO'),
        ('CO14', 'Cultura Organizacional', 'CERIMÔNIAS', 'Reuniões de resultado incluem aprendizados (o que manter, o que ajustar).', 'NÃO'),
        ('CO15', 'Cultura Organizacional', 'POLÍTICAS', 'Políticas internas são conhecidas e aplicadas (não ficam só no papel).', 'NÃO'),
        ('CO16', 'Cultura Organizacional', 'POLÍTICAS', 'Existe canal de denúncia acessível e confiável.', 'NÃO'),
        ('CO17', 'Cultura Organizacional', 'SISTEMAS', 'Sistemas suportam o trabalho (não criam retrabalho ou gargalos).', 'NÃO'),
        ('CO18', 'Cultura Organizacional', 'SISTEMAS', 'Indicadores de pessoas e segurança são acompanhados periodicamente.', 'NÃO'),
        ('CO19', 'Cultura Organizacional', 'JARGÃO/LINGUAGEM', 'A linguagem interna é respeitosa e inclusiva.', 'NÃO'),
        ('CO20', 'Cultura Organizacional', 'JARGÃO/LINGUAGEM', 'Termos e siglas são explicados para evitar exclusão.', 'NÃO'),
        ('CO21', 'Cultura Organizacional', 'CLIMA ORGANIZACIONAL', 'Sinto segurança psicológica para expor opiniões e erros.', 'NÃO'),
        ('CO22', 'Cultura Organizacional', 'CLIMA ORGANIZACIONAL', 'Consigo equilibrar trabalho e vida pessoal.', 'NÃO'),
        ('ESGS01', 'ESG — Pilar Social', 'Diversidade & Inclusão', 'Práticas de contratação e promoção são justas e inclusivas.', 'NÃO'),
        ('ESGS02', 'ESG — Pilar Social', 'Diversidade & Inclusão', 'A empresa promove ambientes livres de assédio e discriminação.', 'NÃO'),
        ('ESGS03', 'ESG — Pilar Social', 'Saúde & Bem-estar', 'Tenho acesso a ações de saúde/apoio emocional quando preciso.', 'NÃO'),
        ('ESGS04', 'ESG — Pilar Social', 'Saúde & Bem-estar', 'Carga de trabalho é ajustada para prevenir sobrecarga crônica.', 'NÃO'),
        ('ESGS05', 'ESG — Pilar Social', 'Desenvolvimento & Capacitação', 'Recebo treinamentos relevantes ao meu perfil de risco e função.', 'NÃO'),
        ('ESGS06', 'ESG — Pilar Social', 'Desenvolvimento & Capacitação', 'Tenho oportunidades reais de desenvolvimento profissional.', 'NÃO'),
        ('ESGS07', 'ESG — Pilar Social', 'Diálogo & Participação', 'Sou ouvido(a) nas decisões que afetam meu trabalho.', 'NÃO'),
        ('ESGS08', 'ESG — Pilar Social', 'Diálogo & Participação', 'A comunicação interna é clara e no tempo certo.', 'NÃO'),
        ('ESGG01', 'ESG — Governança', 'Ética & Compliance', 'Conheço o Código de Ética e como reportar condutas impróprias.', 'NÃO'),
        ('ESGG02', 'ESG — Governança', 'Ética & Compliance', 'Sinto confiança nos processos de investigação e resposta a denúncias.', 'NÃO'),
        ('ESGG03', 'ESG — Governança', 'Transparência & Accountability', 'Metas e resultados são divulgados com clareza.', 'NÃO'),
        ('ESGG04', 'ESG — Governança', 'Transparência & Accountability', 'Há prestação de contas sobre planos e ações corretivas.', 'NÃO'),
        ('ESGG05', 'ESG — Governança', 'Gestão de Riscos & Controles', 'Riscos relevantes são identificados e acompanhados regularmente.', 'NÃO'),
        ('ESGG06', 'ESG — Governança', 'Gestão de Riscos & Controles', 'Controles internos funcionam e são revisados quando necessário.', 'NÃO'),
        ('ESGG07', 'ESG — Governança', 'Documentação PGR/Planos', 'Inventário de riscos e planos de ação (PGR) estão atualizados e acessíveis.', 'NÃO'),
        ('ESGG08', 'ESG — Governança', 'Documentação PGR/Planos', 'Mudanças de processo passam por avaliação de risco antes da implantação.', 'NÃO'),
        ('ESGG09', 'ESG — Governança', 'Canais de Denúncia', 'O canal de denúncia é acessível e protege contra retaliações.', 'NÃO'),
        ('ESGG10', 'ESG — Governança', 'Canais de Denúncia', 'Sinto que denúncias geram ações efetivas.', 'NÃO'),
        ('NR101', 'NR-1 — GRO/PGR', 'Identificação de perigos', 'Tenho meios simples para reportar incidentes/quase-acidentes e perigos.', 'NÃO'),
        ('NR102', 'NR-1 — GRO/PGR', 'Avaliação de riscos', 'No meu posto, riscos são avaliados considerando exposição e severidade x probabilidade.', 'NÃO'),
        ('NR103', 'NR-1 — GRO/PGR', 'Hierarquia de controles', 'A empresa prioriza eliminar/substituir riscos antes de recorrer ao EPI.', 'NÃO'),
        ('NR104', 'NR-1 — GRO/PGR', 'Treinamentos & Mudanças', 'Recebo treinamento quando há mudanças de função/processo/equipamentos.', 'NÃO'),
        ('NR105', 'NR-1 — GRO/PGR', 'Inspeções & Observações', 'Há inspeções/observações de segurança com frequência adequada.', 'NÃO'),
        ('NR106', 'NR-1 — GRO/PGR', 'Comunicação de riscos', 'Sinalização e procedimentos são claros e atualizados.', 'NÃO'),
        ('NR107', 'NR-1 — GRO/PGR', 'Participação dos trabalhadores', 'Sou convidado(a) a participar das discussões de riscos e soluções.', 'NÃO'),
        ('NR108', 'NR-1 — GRO/PGR', 'Emergências & Investigação', 'Planos de emergência são conhecidos e incidentes são investigados com ações corretivas.', 'NÃO'),
        ('FRPS01', 'Fatores de Risco Psicossocial (FRPS)', 'Assédio', 'No meu ambiente há piadas, constrangimentos ou condutas indesejadas.', 'SIM'),
        ('FRPS02', 'Fatores de Risco Psicossocial (FRPS)', 'Assédio', 'Tenho receio de represálias ao reportar assédio ou condutas impróprias.', 'SIM'),
        ('FRPS03', 'Fatores de Risco Psicossocial (FRPS)', 'Relacionamentos', 'Conflitos entre áreas/pessoas permanecem sem solução por muito tempo.', 'SIM'),
        ('FRPS04', 'Fatores de Risco Psicossocial (FRPS)', 'Relacionamentos', 'Falta respeito nas interações do dia a dia.', 'SIM'),
        ('FRPS05', 'Fatores de Risco Psicossocial (FRPS)', 'Comunicação Difícil', 'Falta de informações atrapalha minha entrega.', 'SIM'),
        ('FRPS06', 'Fatores de Risco Psicossocial (FRPS)', 'Comunicação Difícil', 'Mensagens importantes chegam tarde ou de forma confusa.', 'SIM'),
        ('FRPS07', 'Fatores de Risco Psicossocial (FRPS)', 'Remoto/Isolado', 'Trabalho frequentemente isolado sem suporte adequado.', 'SIM'),
        ('FRPS08', 'Fatores de Risco Psicossocial (FRPS)', 'Remoto/Isolado', 'Em teletrabalho me sinto desconectado(a) da equipe.', 'SIM'),
        ('FRPS09', 'Fatores de Risco Psicossocial (FRPS)', 'Excesso de Demandas', 'A sobrecarga e prazos incompatíveis são frequentes.', 'SIM'),
        ('FRPS10', 'Fatores de Risco Psicossocial (FRPS)', 'Excesso de Demandas', 'As expectativas de produtividade são irreais no meu contexto.', 'SIM'),
    ]
    df = pd.DataFrame(data, columns=["Código", "Dimensão", "Subcategoria", "Item", "Reverso"])
    return df

# --- INICIALIZAÇÃO E FORMULÁRIO DINÂMICO ---
df_itens = carregar_itens()
if 'respostas' not in st.session_state:
    st.session_state.respostas = {}

st.subheader("Questionário")
dimensoes = df_itens["Dimensão"].unique().tolist()
def registrar_resposta(item_id, key):
    st.session_state.respostas[item_id] = st.session_state[key]

# O loop abaixo é o responsável pela alteração
for dimensao in dimensoes:
    df_dimensao = df_itens[df_itens["Dimensão"] == dimensao]
    
    # Esta linha extrai a sigla (ex: 'CO', 'ESGS') a partir do código ('CO01', 'ESGS01')
    prefixo_dimensao = df_dimensao['Código'].iloc[0][:-2] if not df_dimensao.empty else dimensao
    
    # A variável 'prefixo_dimensao' é usada como o título do cabeçalho
    with st.expander(f"{prefixo_dimensao}", expanded=True):
        for _, row in df_dimensao.iterrows():
            item_id = row["Código"]
            label = f'({item_id}) {row["Item"]}' + (' (R)' if row["Reverso"] == 'SIM' else '')
            widget_key = f"radio_{item_id}"
            st.radio(
                label, options=["N/A", 1, 2, 3, 4, 5],
                horizontal=True, key=widget_key,
                on_change=registrar_resposta, args=(item_id, widget_key)
            )


# --- BOTÃO DE FINALIZAR E LÓGICA DE RESULTADOS/EXPORTAÇÃO ---
if st.button("Finalizar e Enviar Respostas", type="primary"):
    if not st.session_state.respostas:
        st.warning("Nenhuma resposta foi preenchida.")
    else:
        st.subheader("Resultados e Envio")

        # --- LÓGICA DE CÁLCULO ---
        respostas_list = []
        for index, row in df_itens.iterrows():
            item_id = row['Código']
            resposta_usuario = st.session_state.respostas.get(item_id)
            respostas_list.append({
                "Código": item_id, "Dimensão": row["Dimensão"], "Subcategoria": row["Subcategoria"],
                "Item": row["Item"], "Resposta": resposta_usuario, "Reverso": row["Reverso"]
            })
        dfr = pd.DataFrame(respostas_list)

        with st.spinner("Enviando dados para a planilha..."):
            try:
                # 1. Preparar dados das respostas
                timestamp_str = datetime.now().isoformat(timespec="seconds")
                respostas_para_enviar = []
                for _, row in dfr.iterrows():
                    respostas_para_enviar.append([
                        timestamp_str,
                        respondente,
                        data,
                        organizacao_coletora,
                        row["Dimensão"],
                        row["Subcategoria"],
                        row["Item"],
                        row["Resposta"] if pd.notna(row["Resposta"]) else "N/A"
                    ])
                
                ws_respostas.append_rows(respostas_para_enviar, value_input_option='USER_ENTERED')
        
                st.success("Suas respostas foram enviadas com sucesso!")
                st.balloons()
            except Exception as e:
                st.error(f"Erro ao enviar dados para a planilha: {e}")

                with st.container():
                    st.markdown('<div id="autoclick-div">', unsafe_allow_html=True)
                    if st.button("Ping Button", key="autoclick_button"):
                    # A ação aqui pode ser um simples print no log do Streamlit
                      print("Ping button clicked by automation.")
                    st.markdown('</div>', unsafe_allow_html=True)