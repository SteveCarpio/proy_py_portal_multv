import streamlit as st
import gc
import base64
import random
import importlib
from datetime import datetime, timedelta
from PIL import Image

# -------------------------
# ⚙️ CONFIG
# -------------------------
st.set_page_config(
    page_title="Portal TDA: [ MULTIVA ]",
    page_icon="🤖",
    layout="wide"
)

# -------------------------
# 🎨 CARGAR CSS
# -------------------------
def load_css():
    with open("styles/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# -------------------------
# 🔐 LOGIN (7 días)
# -------------------------
SESSION_DAYS = 7

def login_web():

    if "auth" not in st.session_state:
        st.session_state.auth = False
        st.session_state.login_time = None
        st.session_state.user = None

    # Validar sesión existente
    if st.session_state.auth:
        if st.session_state.login_time:
            if datetime.now() - st.session_state.login_time < timedelta(days=SESSION_DAYS):
                return True
            else:
                st.session_state.auth = False

    # UI LOGIN
    st.title("🔐 Login Portal TDA")

    user = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        users = st.secrets["auth"]

        if user in users and users[user] == password:
            st.session_state.auth = True
            st.session_state.login_time = datetime.now()
            st.session_state.user = user
            st.rerun()
        else:
            st.error("Credenciales incorrectas")

    return False

# -------------------------
# 🔓 LOGOUT
# -------------------------
def logout_button():
    if st.sidebar.button("🔓 Cerrar sesión"):
        st.session_state.auth = False
        st.session_state.login_time = None
        st.session_state.user = None
        st.rerun()

# -------------------------
# 🔧 HELPERS
# -------------------------
def get_image_base64(path):
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""

def card(titulo, texto):
    return f'''
    <div class="card-base app-card">
        <p class="tag-ia">{titulo}</p>
        <p class="small-text-fin">{texto}</p>
    </div>
    '''

# -------------------------
# 📊 APPS
# -------------------------
IA_APPS = {"Emisores": "app1"}
DS_APPS = {"Listado Historico": "app2"}
WS_APPS = {"Trimestrales": "app3"}
RP_APPS = {"Publicaciones": "app4", "Festivos": "app5"}
GP_APPS = {"Semanales / Mensuales": "app6"}
XX_APPS = {"Bolsa-MX": "app7", "Global": "app8"}

TODAS_LAS_APPS = {**IA_APPS, **DS_APPS, **WS_APPS, **RP_APPS, **GP_APPS, **XX_APPS}

# -------------------------
# 🏠 HOME
# -------------------------
def mostrar_inicio():

    col1, col2 = st.columns([3,1])

    with col1:
        st.markdown('''
        <div class="card-base banner">
            <p class="banner-titulo">📢 Noticias</p>
            <p class="small-text-fin">BMV 5% - Multiva 0.5%</p>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        try:
            st.image(Image.open("img/logo_multiva2.png"))
        except Exception:
            pass

    st.markdown('<h4 class="tag-ia">Bienvenido al portal TDA</h4>', unsafe_allow_html=True)

    st.markdown('<h3 class="section-title">🏛️ Fideicomisos</h3>', unsafe_allow_html=True)
    st.markdown(card("Emisores", "Datos..."), unsafe_allow_html=True)

    st.markdown('<h3 class="section-title">🚨 Eventos</h3>', unsafe_allow_html=True)
    st.markdown(card("Histórico", "..."), unsafe_allow_html=True)

# -------------------------
# 🚀 INICIO APP
# -------------------------
load_css()

if not login_web():
    st.stop()

logout_button()

USER_IP = st.context.ip_address

if "selected_app_key" not in st.session_state:
    st.session_state.selected_app_key = None

# SIDEBAR
if st.session_state.selected_app_key is None:

    cats = {
        "Fideicomisos": IA_APPS,
        "Eventos": DS_APPS
    }

    for titulo, dicc in cats.items():
        with st.sidebar.expander(titulo):
            for name in dicc:
                if st.button(name):
                    st.session_state.selected_app_key = name
                    st.rerun()

# CONTENIDO
if st.session_state.selected_app_key:
    app_name = st.session_state.selected_app_key
    archivo = TODAS_LAS_APPS.get(app_name)

    if archivo:
        try:
            modulo = importlib.import_module(f"app.{archivo}")
            importlib.reload(modulo)
            modulo.main()
        except Exception as e:
            st.error(e)

    gc.collect()

else:
    mostrar_inicio()

# FOOTER SIDEBAR
st.sidebar.markdown("---")
st.sidebar.text(f"IP: {USER_IP}")