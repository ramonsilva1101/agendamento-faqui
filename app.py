import streamlit as st
import pandas as pd
import urllib.parse
import requests
from datetime import datetime

# 1. CONFIGURAÇÃO DA PÁGINA (Deve ser a primeira coisa do Streamlit)
st.set_page_config(page_title="Sistema de Agendamento FAQUI", page_icon="📅", layout="centered")

# 2. SISTEMA DE LOGIN SEGURO DO GOOGLE (Puxa do "Cofre" do Streamlit)
try:
    CLIENT_ID = st.secrets["GOOGLE_CLIENT_ID"]
    CLIENT_SECRET = st.secrets["GOOGLE_CLIENT_SECRET"]
    REDIRECT_URI = st.secrets["REDIRECT_URI"]
except:
    st.error("Erro: Chaves de segurança não encontradas nos Secrets do Streamlit.")
    st.stop()

AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USER_INFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"

# Inicia a sessão
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# Lógica para processar o retorno do Google
query_params = st.query_params
if "code" in query_params and st.session_state.user_email is None:
    code = query_params["code"]
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    res = requests.post(TOKEN_URL, data=data)
    if res.status_code == 200:
        access_token = res.json().get("access_token")
        headers = {"Authorization": f"Bearer {access_token}"}
        user_info = requests.get(USER_INFO_URL, headers=headers).json()
        st.session_state.user_email = user_info.get("email")
        st.query_params.clear()
        st.rerun()

# --- TELA DE LOGIN (VISUAL NOVO) ---
if st.session_state.user_email is None:
    # CSS para esconder menus e centralizar
    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        body { background-color: #f8f9fa; }
        </style>
        """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("")
        st.write("")
        # Tenta carregar a logo
        try:
            st.image("logo.png", use_container_width=True)
        except:
            st.markdown("<h1 style='text-align: center; color: #1f2937;'>FAQUI</h1>", unsafe_allow_html=True)
        
        st.markdown("<h2 style='text-align: center; color: #1f2937; margin-bottom: 5px;'>Portal do Professor</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #6b7280; font-size: 16px; margin-bottom: 30px;'>Acesso restrito ao Sistema de Agendamento.</p>", unsafe_allow_html=True)
        
        # Link do botão
        params = {
            "client_id": CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
            "prompt": "select_account"
        }
        login_url = f"{AUTHORIZATION_URL}?{urllib.parse.urlencode(params)}"
        
        google_logo = "https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg"
        button_html = f'''
        <div style="display: flex; justify-content: center;">
            <a href="{login_url}" target="_self" style="text-decoration: none;">
                <button style="background-color: white; color: #757575; padding: 12px 24px; border: 1px solid #ddd; border-radius: 4px; cursor: pointer; font-size: 16px; font-weight: 500; display: flex; align-items: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <img src="{google_logo}" style="width: 20px; height: 20px; margin-right: 12px;">
                    Entrar com o Google
                </button>
            </a>
        </div>
        '''
        st.markdown(button_html, unsafe_allow_html=True)
    st.stop()

# --- ÁREA LOGADA (SISTEMA DE AGENDAMENTO) ---

st.sidebar.image("logo.png", width=100)
st.sidebar.title("Menu")
st.sidebar.write(f"👤 **Usuário:**\n{st.session_state.user_email}")

if st.sidebar.button("Sair"):
    st.session_state.user_email = None
    st.rerun()

st.title("📅 Agendamento de Recursos")

# Exemplo de fluxo de agendamento
recurso = st.selectbox("Selecione o Recurso:", ["Projetor 01", "Auditório", "Laboratório de TI", "Laboratório de Saúde"])
data_reserva = st.date_input("Data da Reserva:", datetime.now())
horario = st.time_input("Horário:")

if st.button("Confirmar Agendamento"):
    # Aqui você conectaria com o seu banco de dados ou planilha
    st.success(f"Sucesso! {recurso} reservado para {st.session_state.user_email} em {data_reserva} às {horario}.")
    st.balloons()

# Mostrar agendamentos (Exemplo visual)
st.divider()
st.subheader("Seus Agendamentos")
# Aqui entraria um st.dataframe(df) com os dados reais
st.info("Você ainda não possui agendamentos para esta semana.")