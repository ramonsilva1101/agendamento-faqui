import streamlit as st
import pandas as pd
import urllib.parse
import requests
from datetime import datetime

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Sistema de Agendamento FAQUI", page_icon="📅", layout="centered")

# 2. CONFIGURAÇÕES DE SEGURANÇA (GOOGLE)
try:
    CLIENT_ID = st.secrets["GOOGLE_CLIENT_ID"]
    CLIENT_SECRET = st.secrets["GOOGLE_CLIENT_SECRET"]
    REDIRECT_URI = st.secrets["REDIRECT_URI"]
except:
    st.error("Erro: Configure os Secrets no painel do Streamlit.")
    st.stop()

AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USER_INFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"

if "user_email" not in st.session_state:
    st.session_state.user_email = None

# Processar o retorno do Google
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

# --- TELA DE LOGIN ESTILIZADA ---
if st.session_state.user_email is None:
    # Injeção de CSS para o Card e esconder menus
    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Fundo da tela */
        .stApp {
            background-color: #f0f2f5;
        }

        /* Estilo do Card */
        .login-card {
            background-color: #ffffff;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            text-align: center;
            max-width: 400px;
            margin: auto;
        }
        
        .azul-faqui {
            color: #004A8D; /* Azul Institucional - ajuste se necessário */
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)

    # Centralização vertical manual
    st.write("")
    st.write("")
    st.write("")

    # Construção do Card em HTML
    # Note que para a imagem funcionar dentro do HTML, o Streamlit prefere st.image
    # Então vamos dividir o card em partes:
    
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        with st.container():
            # Início do Card (HTML)
            st.markdown('<div class="login-card">', unsafe_allow_html=True)
            
            # Logo
            try:
                st.image("static/logo.png", width=180)
            except:
                st.markdown("<h1 style='color: #004A8D;'>FAQUI</h1>", unsafe_allow_html=True)
            
            # Textos
            st.markdown("<h2 class='azul-faqui' style='margin-top: 20px;'>Portal do Professor</h2>", unsafe_allow_html=True)
            st.markdown("<p style='color: #6b7280; margin-bottom: 30px;'>Acesso restrito ao Sistema de Agendamento.</p>", unsafe_allow_html=True)
            
            # Botão do Google
            params = {
                "client_id": CLIENT_ID, "redirect_uri": REDIRECT_URI,
                "response_type": "code", "scope": "openid email profile",
                "access_type": "offline", "prompt": "select_account"
            }
            login_url = f"{AUTHORIZATION_URL}?{urllib.parse.urlencode(params)}"
            google_logo = "https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg"
            
            st.markdown(f'''
                <a href="{login_url}" target="_self" style="text-decoration: none;">
                    <div style="display: flex; align-items: center; justify-content: center; background-color: white; color: #757575; padding: 10px; border: 1px solid #ddd; border-radius: 5px; cursor: pointer; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <img src="{google_logo}" style="width: 18px; height: 18px; margin-right: 10px;">
                        <span style="font-size: 14px; font-weight: 500; font-family: 'Roboto', sans-serif;">Entrar com o Google</span>
                    </div>
                </a>
            ''', unsafe_allow_html=True)
            
            # Fim do Card
            st.markdown('</div>', unsafe_allow_html=True)
            
    st.stop()

# --- ÁREA LOGADA ---
st.sidebar.image("static/logo.png", width=120)
st.sidebar.markdown(f"👤 **Bem-vindo(a)**\n\n{st.session_state.user_email}")

if st.sidebar.button("Sair do Sistema"):
    st.session_state.user_email = None
    st.rerun()

st.title("📅 Agendamento de Recursos - FAQUI")
st.info("O sistema está pronto. Aguardando liberação de acesso no Google Admin.")

# Aqui você pode continuar desenvolvendo a lógica de agendamento na segunda-feira.