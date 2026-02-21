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

# --- TELA DE LOGIN (CARD BRANCO COM FUNDO AZUL) ---
if st.session_state.user_email is None:
    # Injeção de CSS Avançado para Centralização Total e Cores
    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Fundo Azul Institucional */
        .stApp {
            background: linear-gradient(135deg, #004A8D 0%, #002D57 100%);
            display: flex;
            justify-content: center;
            align-items: center;
        }

        /* Container Principal do Card */
        .main-container {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
        }

        /* Estilo do Card Branco */
        .login-card {
            background-color: #ffffff;
            padding: 50px 30px;
            border-radius: 20px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            text-align: center;
            width: 100%;
            max-width: 400px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        /* Ajuste da logo dentro do card */
        .logo-img {
            max-width: 200px;
            margin-bottom: 20px;
        }

        .titulo-login {
            color: #004A8D;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
            font-family: 'sans-serif';
        }

        .subtitulo-login {
            color: #6b7280;
            font-size: 14px;
            margin-bottom: 30px;
        }
        </style>
        """, unsafe_allow_html=True)

    # Construção do Layout centralizado usando Colunas para "empurrar" pro meio
    empty1, central_col, empty2 = st.columns([0.1, 0.8, 0.1])
    
    with central_col:
        # Iniciamos o Card
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        # Logo Centralizada (usamos st.image com container_width=False para não esticar)
        try:
            st.image("static/logo.png", width=220)
        except:
            st.markdown("<h1 style='color: #004A8D;'>FAQUI</h1>", unsafe_allow_html=True)
        
        # Textos do Card
        st.markdown("<div class='titulo-login'>Portal do Professor</div>", unsafe_allow_html=True)
        st.markdown("<div class='subtitulo-login'>Acesso restrito ao Sistema de Agendamento.</div>", unsafe_allow_html=True)
        
        # Botão do Google
        params = {
            "client_id": CLIENT_ID, "redirect_uri": REDIRECT_URI,
            "response_type": "code", "scope": "openid email profile",
            "access_type": "offline", "prompt": "select_account"
        }
        login_url = f"{AUTHORIZATION_URL}?{urllib.parse.urlencode(params)}"
        google_logo = "https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg"
        
        st.markdown(f'''
            <a href="{login_url}" target="_self" style="text-decoration: none; width: 100%;">
                <div style="display: flex; align-items: center; justify-content: center; background-color: white; color: #757575; padding: 12px; border: 1px solid #ddd; border-radius: 8px; cursor: pointer; box-shadow: 0 1px 2px rgba(0,0,0,0.1); width: 100%;">
                    <img src="{google_logo}" style="width: 20px; height: 20px; margin-right: 12px;">
                    <span style="font-size: 16px; font-weight: 500; font-family: 'Roboto', sans-serif;">Entrar com o Google</span>
                </div>
            </a>
        ''', unsafe_allow_html=True)
        
        # Fechamos o Card
        st.markdown('</div>', unsafe_allow_html=True)
            
    st.stop()

# --- ÁREA LOGADA (O QUE APARECE APÓS O LOGIN) ---
st.sidebar.image("static/logo.png", width=120)
st.sidebar.markdown(f"👤 **Bem-vindo(a)**\n\n{st.session_state.user_email}")

if st.sidebar.button("Sair do Sistema"):
    st.session_state.user_email = None
    st.rerun()

st.title("📅 Painel de Agendamento")
st.write("Selecione o recurso e o horário desejado.")
# ... restante do seu código de agendamento ...