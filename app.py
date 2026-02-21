import streamlit as st
import urllib.parse
import requests

# --- SISTEMA DE LOGIN SEGURO DO GOOGLE ---
# Puxa as chaves do cofre do Streamlit
CLIENT_ID = st.secrets["GOOGLE_CLIENT_ID"]
CLIENT_SECRET = st.secrets["GOOGLE_CLIENT_SECRET"]
REDIRECT_URI = st.secrets["REDIRECT_URI"]

AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USER_INFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"

# Inicia a sessão do usuário
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# Verifica se o Google devolveu o código de acesso na URL
query_params = st.query_params
if "code" in query_params and st.session_state.user_email is None:
    code = query_params["code"]
    
    # Troca o código pela identidade do usuário
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
        
        # Salva o e-mail logado e limpa a URL
        st.session_state.user_email = user_info.get("email")
        st.query_params.clear()
        st.rerun()

# --- TELA DE BLOQUEIO (Se não estiver logado) ---
if st.session_state.user_email is None:
    st.title("📅 Sistema de Agendamento - FAQUI")
    st.warning("Acesso restrito. Por favor, faça login com seu e-mail institucional (@faqui.edu.br).")
    
    # Cria o link do botão do Google
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "select_account"
    }
    login_url = f"{AUTHORIZATION_URL}?{urllib.parse.urlencode(params)}"
    
    # Botão azul bonito
    st.markdown(f'<a href="{login_url}" target="_self"><button style="background-color:#4285F4;color:white;padding:10px 20px;border:none;border-radius:5px;cursor:pointer;font-size:16px;font-weight:bold;">Entrar com o Google</button></a>', unsafe_allow_html=True)
    
    st.stop() # 🚨 Isso para o código aqui. O resto do site não carrega sem login!

# --- SISTEMA LIBERADO ---
# A partir daqui, o código do seu sistema de agendamento continua normalmente!
# O e-mail do professor logado agora está guardado na variável: st.session_state.user_email

st.sidebar.success(f"Logado como: {st.session_state.user_email}")