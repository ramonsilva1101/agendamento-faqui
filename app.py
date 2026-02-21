import streamlit as st
import os
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import base64
import banco_dados

# 1. Configuração da página (LAYOUT WIDE)
st.set_page_config(page_title="Agendamento TI", page_icon="💻", layout="wide")
banco_dados.criar_banco()

# --- CSS PERSONALIZADO (BARRA LATERAL TRANSLÚCIDA) ---
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: rgba(53, 58, 133, 0.15) !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÃO DE USUÁRIOS E ADMIN ---
EMAIL_ADMIN = "ti@faculdade.edu.br"
emails_permitidos = [
    EMAIL_ADMIN,
    "professor.joao@faculdade.edu.br",
    "coordenadora.maria@faculdade.edu.br",
    "professor.carlos@faculdade.edu.br"
]

# --- BARRA LATERAL: SIMULAÇÃO DE LOGIN ---
st.sidebar.markdown("🔒 **Acesso do Usuário**")
usuario_logado = st.sidebar.selectbox("E-mail:", emails_permitidos)

# --- BARRA LATERAL: MENU DE RESERVA ---
st.sidebar.markdown("📅 **Faça sua Reserva**")

# CORREÇÃO: As variáveis de data voltaram para cá!
data_hoje = datetime.date.today()
data_limite = data_hoje + relativedelta(months=+6)

recurso_selecionado = st.sidebar.selectbox(
    "Recurso:",
    ["Caixa de Som 1", "Caixa de Som 2", "Laboratório de Informática", "Sala 360", "Estúdio"]
)

data_escolhida = st.sidebar.date_input(
    "Data:",
    value=data_hoje,
    min_value=data_hoje,
    max_value=data_limite,
    format="DD/MM/YYYY" 
)

horarios_aulas = [
    "19:00 - 19:50 (1ª Aula)", 
    "19:50 - 20:40 (2ª Aula)", 
    "20:55 - 21:45 (3ª Aula)", 
    "21:45 - 22:35 (4ª Aula)"
]
horario_escolhido = st.sidebar.selectbox("Horário:", horarios_aulas)

if st.sidebar.button("Confirmar Agendamento", type="primary", use_container_width=True):
    esta_livre = banco_dados.verificar_disponibilidade(recurso_selecionado, data_escolhida, horario_escolhido)
    if esta_livre == True:
        banco_dados.salvar_reserva(recurso_selecionado, data_escolhida, horario_escolhido, usuario_logado)
        st.sidebar.success("✅ Reserva realizada com sucesso!")
        st.rerun()
    else:
        st.sidebar.error("❌ Ops! Já reservado.")

# --- BARRA LATERAL: LOGO E CRÉDITOS DO DESENVOLVEDOR ---
caminho_imagem = "static/logo.png"
if not os.path.exists(caminho_imagem):
    caminho_imagem = "static/logo.png.png" 

if os.path.exists(caminho_imagem):
    with open(caminho_imagem, "rb") as img_file:
        img_b64 = base64.b64encode(img_file.read()).decode()
    
    html_logo_footer = f'''
    <div style="text-align: center; margin-top: 10px;">
        <img src="data:image/png;base64,{img_b64}" width="70%">
    </div>
    <div style="background-color: #353A85; padding: 8px; border-radius: 6px; text-align: center; color: white; margin-top: 10px; box-shadow: 0px 2px 4px rgba(0,0,0,0.1);">
        <p style="margin: 0; font-size: 0.85rem; font-weight: 500;">Desenvolvido por <b>Ramon Silva</b></p>
    </div>
    '''
    st.sidebar.markdown(html_logo_footer, unsafe_allow_html=True)
else:
    st.sidebar.warning("⚠️ Logo não encontrada.")

# ==========================================
# --- TELA PRINCIPAL (BANNER CLEAN PREMIUM) ---
# ==========================================

html_titulo_premium = f"""
<div style="
    background-color: #FFFFFF;
    padding: 35px;
    border-radius: 12px;
    box-shadow: 0px 8px 24px rgba(0,0,0,0.06);
    text-align: center;
    margin-bottom: 30px;
    border-top: 6px solid #353A85;
">
    <h1 style="color: #212529; margin: 0; font-size: 2.6rem; font-weight: 700; letter-spacing: -0.5px;">
        Reservas: Equipamentos e Salas
    </h1>
    <div style="
        margin-top: 20px; 
        display: inline-block; 
        background-color: #F8F9FA; 
        border: 1px solid #E9ECEF;
        padding: 8px 20px; 
        border-radius: 25px; 
        color: #495057; 
        font-size: 0.95rem;
    ">
        👤 Logado como: <b>{usuario_logado}</b>
    </div>
</div>
"""
st.markdown(html_titulo_premium, unsafe_allow_html=True)

# --- SESSÃO 1: CALENDÁRIO VISUAL DE DISPONIBILIDADE ---
st.markdown(f"<h3 style='text-align: center; color: #353A85;'>📅 Disponibilidade: {recurso_selecionado}</h3>", unsafe_allow_html=True)
st.write("Verifique abaixo os dias e horários livres para os próximos 15 dias.")

dias_grid = [data_hoje + datetime.timedelta(days=i) for i in range(15)]
df_grid = pd.DataFrame(index=[d.strftime("%Y-%m-%d") for d in dias_grid], columns=horarios_aulas)
df_grid.fillna("Livre", inplace=True) 

reservas_recurso = banco_dados.listar_reservas_por_recurso(recurso_selecionado)

for res in reservas_recurso:
    data_res = res[0]
    horario_res = res[1]
    if data_res in df_grid.index and horario_res in df_grid.columns:
        df_grid.at[data_res, horario_res] = "Reservado"

df_grid.index = [datetime.datetime.strptime(d, "%Y-%m-%d").strftime("%d/%m/%Y") for d in df_grid.index]

def pintar_tabela(valor):
    if valor == "Reservado":
        return 'background-color: #353A85; color: white; font-weight: bold;'
    return 'background-color: #FFFFFF; color: #212529;'

try:
    tabela_colorida = df_grid.style.map(pintar_tabela)
except AttributeError:
    tabela_colorida = df_grid.style.applymap(pintar_tabela)

st.dataframe(tabela_colorida, use_container_width=True)

st.divider()

# --- SESSÃO 2: AGENDA GERAL ---
st.markdown("<h3 style='text-align: center; color: #353A85;'>📋 Lista Completa de Reservas</h3>", unsafe_allow_html=True)

dados_reservas = banco_dados.listar_reservas()

if len(dados_reservas) > 0:
    df_lista = pd.DataFrame(dados_reservas, columns=["ID da Reserva", "Recurso", "Data", "Horário", "E-mail do Usuário"])
    df_lista['Data'] = pd.to_datetime(df_lista['Data']).dt.strftime('%d/%m/%Y')
    st.dataframe(df_lista, hide_index=True, use_container_width=True)
else:
    st.info("Nenhuma reserva encontrada. A agenda está livre!")

st.divider()

# --- SESSÃO 3: CANCELAMENTO ---
st.markdown("<h3 style='text-align: center; color: #353A85;'>🗑️ Cancelar Reserva</h3>", unsafe_allow_html=True)

if usuario_logado == EMAIL_ADMIN:
    reservas_para_cancelar = dados_reservas
    st.caption("🛡️ Modo Admin Ativo: Você pode cancelar a reserva de qualquer usuário.")
else:
    reservas_para_cancelar = [reserva for reserva in dados_reservas if reserva[4] == usuario_logado]

if len(reservas_para_cancelar) > 0:
    opcoes_cancelamento = {
        f"ID {r[0]} - {r[1]} no dia {r[2]} ({r[3]})": r[0] for r in reservas_para_cancelar
    }
    
    col_canc1, col_canc2 = st.columns([2, 1])
    with col_canc1:
        reserva_selecionada = st.selectbox("Selecione a reserva que deseja cancelar:", list(opcoes_cancelamento.keys()))
    with col_canc2:
        st.write("") 
        st.write("")
        if st.button("🚨 Cancelar Reserva Selecionada"):
            id_para_deletar = opcoes_cancelamento[reserva_selecionada]
            banco_dados.deletar_reserva(id_para_deletar)
            st.success("✅ Reserva cancelada com sucesso!")
            st.rerun()
else:
    st.write("Você não possui reservas ativas para cancelar.")