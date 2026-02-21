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
    st.error("Erro: Configure os Secrets no painel do Streamlit (Client ID e Secret).")
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
    # CSS para Centralização Absoluta e Fundo Roxo Degradê
    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Fundo com degradê roxo/azul institucional */
        .stApp {
            background: linear-gradient(135deg, #2D1B4E 0%, #161B33 100%) !important;
        }

        /* Container para centralizar o card na vertical e horizontal */
        .main-wrapper {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 85vh;
        }

        /* O Card Branco Flutuante */
        .login-card {
            background-color: #ffffff;
            padding: 50px 40px;
            border-radius: 24px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.4);
            text-align: center;
            width: 100%;
            max-width: 400px;
        }

        .titulo-card {
            color: #2D1B4E; /* Roxo escuro para contraste */
            font-size: 26px;
            font-weight: 800;
            margin-top: 20px;
            margin-bottom: 8px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        .texto-card {
            color: #64748b;
            font-size: 15px;
            margin-bottom: 35px;
            line-height: 1.5;
        }

        /* Ajuste fino para o botão do Google */
        .google-btn-container {
            display: flex;
            justify-content: center;
            width: 100%;
        }
        </style>
        """, unsafe_allow_html=True)

    # Início do Layout
    st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    
    # Carregamento da Logo em Base64 para garantir exibição dentro do Card
    try:
        with open("static/logo.png", "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
            st.markdown(f'<img src="data:image/png;base64,{data}" style="max-width: 180px; height: auto;">', unsafe_allow_html=True)
    except:
        st.markdown("<h1 style='color: #2D1B4E;'>FAQUI</h1>", unsafe_allow_html=True)

    # Conteúdo do Card
    st.markdown('<div class="titulo-card">Portal do Professor</div>', unsafe_allow_html=True)
    st.markdown('<div class="texto-card">Sistema de Agendamento de Recursos.<br>Identifique-se para continuar.</div>', unsafe_allow_html=True)

    # Botão de Login do Google
    params = {
        "client_id": CLIENT_ID, "redirect_uri": REDIRECT_URI,
        "response_type": "code", "scope": "openid email profile",
        "access_type": "offline", "prompt": "select_account"
    }
    login_url = f"{AUTHORIZATION_URL}?{urllib.parse.urlencode(params)}"
    google_logo = "https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg"

    st.markdown(f'''
        <a href="{login_url}" target="_self" style="text-decoration: none;">
            <div style="display: flex; align-items: center; justify-content: center; background-color: white; color: #3c4043; padding: 12px 24px; border: 1px solid #dadce0; border-radius: 8px; cursor: pointer; transition: background-color .2s; box-shadow: 0 1px 2px rgba(60,64,67,0.3);">
                <img src="{google_logo}" style="width: 20px; height: 20px; margin-right: 12px;">
                <span style="font-size: 16px; font-weight: 500; font-family: 'Google Sans',Roboto,Arial,sans-serif;">Entrar com o Google</span>
            </div>
        </a>
    ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True) # Fecha Card
    st.markdown('</div>', unsafe_allow_html=True) # Fecha Wrapper
            
    st.stop()

# --- ÁREA LOGADA (PAINEL INTERNO) ---
st.sidebar.image("static/logo.png", width=120)
st.sidebar.markdown(f"**Professor(a):**\n{st.session_state.user_email}")

if st.sidebar.button("Encerrar Sessão"):
    st.session_state.user_email = None
    st.rerun()

st.title("📅 Painel de Agendamento")
st.write("Bem-vindo ao sistema de agendamento da FAQUI.")

# Exemplo de formulário de reserva
col_a, col_b = st.columns(2)
with col_a:
    recurso = st.selectbox("Recurso:", ["Laboratório 01", "Projetor", "Auditório"])
with col_b:
    data = st.date_input("Data:", datetime.now())

if st.button("Reservar Agora"):
    st.success(f"Solicitação de {recurso} enviada com sucesso!")