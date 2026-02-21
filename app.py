import streamlit as st
import pandas as pd
import urllib.parse
import requests
import base64
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

# Processar retorno do Google
query_params = st.query_params
if "code" in query_params and st.session_state.user_email is None:
    code = query_params["code"]
    data = {
        "code": code, "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI, "grant_type": "authorization_code"
    }
    res = requests.post(TOKEN_URL, data=data)
    if res.status_code == 200:
        access_token = res.json().get("access_token")
        headers = {"Authorization": f"Bearer {access_token}"}
        user_info = requests.get(USER_INFO_URL, headers=headers).json()
        st.session_state.user_email = user_info.get("email")
        st.query_params.clear()
        st.rerun()

# --- TELA DE LOGIN ESTILO "FLOQ" (CARD CENTRALIZADO) ---
if st.session_state.user_email is None:
    # Lógica para ler a imagem da logo e converter para Base64 (necessário para o HTML)
    try:
        with open("static/logo.png", "rb") as f:
            encoded_logo = base64.b64encode(f.read()).decode()
            logo_html = f'<img src="data:image/png;base64,{encoded_logo}" style="width: 180px; margin-bottom: 20px;">'
    except:
        logo_html = '<h1 style="color: #004A8D; margin-bottom: 20px;">FAQUI</h1>'

    # Link do Google
    params = {
        "client_id": CLIENT_ID, "redirect_uri": REDIRECT_URI,
        "response_type": "code", "scope": "openid email profile",
        "access_type": "offline", "prompt": "select_account"
    }
    login_url = f"{AUTHORIZATION_URL}?{urllib.parse.urlencode(params)}"
    google_icon = "https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg"

    # CSS Customizado
    st.markdown(f"""
        <style>
        #MainMenu {{visibility: hidden;}}
        header {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        
        /* Fundo em degradê roxo/azul */
        .stApp {{
            background: linear-gradient(180deg, #1a2a6c 0%, #2D1B4E 50%, #000000 100%) !important;
        }}

        /* Container Principal */
        .login-wrapper {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            width: 100%;
        }}

        /* O Card estilo FLOQ */
        .login-card {{
            background-color: white;
            padding: 50px 40px;
            border-radius: 25px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
            text-align: center;
            width: 380px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        .welcome-text {{
            color: #333;
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 10px;
            font-family: 'Segoe UI', sans-serif;
        }}

        .sub-text {{
            color: #666;
            font-size: 14px;
            margin-bottom: 40px;
        }}

        .google-btn {{
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: white;
            color: #555;
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 10px;
            text-decoration: none;
            font-weight: 600;
            font-size: 15px;
            transition: 0.3s;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}

        .google-btn:hover {{
            background-color: #f8f9fa;
            border-color: #ccc;
        }}
        </style>

        <div class="login-wrapper">
            <div class="login-card">
                {logo_html}
                <div class="welcome-text">Bem-vindo</div>
                <div class="sub-text">Acesso restrito ao Sistema de Agendamento</div>
                <a href="{login_url}" class="google-btn" target="_self">
                    <img src="{google_icon}" style="width: 20px; margin-right: 15px;">
                    Entrar com o Google
                </a>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# --- ÁREA LOGADA ---
st.title("📅 Painel de Agendamento")
st.sidebar.image("static/logo.png", width=120)
st.sidebar.write(f"Conectado como: {st.session_state.user_email}")
if st.sidebar.button("Sair"):
    st.session_state.user_email = None
    st.rerun()