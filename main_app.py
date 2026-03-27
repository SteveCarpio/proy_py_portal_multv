import streamlit as st
import gc
import base64
import random
import importlib
from datetime import datetime
from PIL import Image

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Portal TDA: [ MULTIVA ]",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. ESTILOS CSS OPTIMIZADOS
st.markdown("""
<style>

/* =========================
   🔹 BASE COMPONENTES
========================= */
.card-base {
    padding: 0.8rem 1rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    transition: transform 0.2s;
    box-shadow: 1px 1px 6px rgba(0,0,0,0.05);
}

/* =========================
   🔹 BANNER
========================= */
.banner {
    background-color: #f0f2f6;
    padding: 0.5rem;
}

.banner-titulo { 
    color: #FF6200; 
    font-weight: bold; 
    font-size: 0.7rem; 
}

/* =========================
   🔹 TARJETAS
========================= */
.app-card {
    background-color: #FFF8F2;
    border-left: 4px solid #1c2e4a;
}

.app-card:hover {
    transform: translateX(5px);
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
}

/* =========================
   🔹 TITULOS
========================= */
.section-title {
    color: #1c2e4a;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-weight: 700;
    border-bottom: 2px solid #e9ecef;
    padding-bottom: 10px;
    margin-top: 20px;
}

.titulo-tda { 
    color: #555; 
    font-size: 0.7rem; 
}

/* =========================
   🔹 TEXTOS
========================= */
.small-text-fin {
    font-size: 0.75rem;
    color: #666;
    line-height: 1.2;
    margin-top: 5px;
}

.tag-ia { 
    color: #FF6200; 
    font-weight: bold; 
    font-size: 0.65rem; 
    text-transform: uppercase; 
    margin: 2px 0;
}

/* =========================
   🔹 SIDEBAR
========================= */
[data-testid="stSidebar"] {
    background-color: #f0f2f6;
}

</style>
""", unsafe_allow_html=True)

# 3. DICCIONARIOS DE APLICACIONES
IA_APPS = {"Emisores": "app1"}
DS_APPS = {"Listado Historico": "app2"}
WS_APPS = {"Trimestrales": "app3"}
RP_APPS = {"Publicaciones": "app4", "Festivos": "app5"}
GP_APPS = {"Semanales / Mensuales   ": "app6"}
XX_APPS = {"Bolsa-MX": "app7", "Global": "app8"}

TODAS_LAS_APPS = {**IA_APPS, **DS_APPS, **WS_APPS, **RP_APPS, **GP_APPS, **XX_APPS}

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
# 🏠 PANTALLA INICIO
# -------------------------
def mostrar_inicio():
    COL_ANCHO = 0.1

    col_t1, col_t2, col_t3 = st.columns([3, COL_ANCHO ,1])

    with col_t1:
        st.markdown('''
        <div class="card-base banner">
            <p class="banner-titulo">📢 [ 2026-03-26 Noticias xxxxx x x x ]</p>
            <p class="small-text-fin">BMV 5% - Multiva 0.5%.</p>
        </div>
        ''', unsafe_allow_html=True)

    with col_t3:
        try:
            logo = Image.open("img/logo_multiva2.png")
            st.image(logo)
        except Exception:
            pass

    st.markdown('<h4><p class="tag-ia">Bienvenido al portal TDA - [ Banco Multiva ]</p></h4>', unsafe_allow_html=True)

    # --- SECCIONES ---
    st.markdown('<h3 class="section-title">🏛️ Fideicomisos y Emisiones</h3>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(card("Emisores", "Datos de Documentos, etc..."), unsafe_allow_html=True)

    st.markdown('<h3 class="section-title">🚨 Eventos Relevantes</h3>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(card("Listado Histórico", "xxxxxxxxxxxx."), unsafe_allow_html=True)

    st.markdown('<h3 class="section-title">📑 Reportes de Emisores</h3>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(card("Trimestrales", "xxxxxxxxxxxx."), unsafe_allow_html=True)

    st.markdown('<h3 class="section-title">📅 Calendario Operativo</h3>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(card("Publicaciones", "xxxxxxxxx."), unsafe_allow_html=True)
    with c2:
        st.markdown(card("Festivos", "xxxxxxxxxxxx."), unsafe_allow_html=True)

    st.markdown('<h3 class="section-title">✅ Tareas Programadas</h3>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(card("Semanales", "xxxxxxxxxxxx."), unsafe_allow_html=True)
    with c2:
        st.markdown(card("Mensuales", "xxxxxxxxxxxx."), unsafe_allow_html=True)

    st.markdown('<h3 class="section-title">📊 Indicadores Económicos</h3>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(card("xxxxx", "xxxxxxxxxxxx."), unsafe_allow_html=True)

    # --- FOOTER ---
    st.markdown("---")
    img_b64 = get_image_base64("img/logotipo.ico")
    if img_b64:
        st.markdown(f"""
        <div style='text-align: center;'>
            <img src='data:image/png;base64,{img_b64}' width='30'>
            <br>
            <small>© {datetime.now().year} Titulización de Activos S.A. - Confidencial</small>
        </div>
        """, unsafe_allow_html=True)

# -------------------------
# 🚀 NAVEGACIÓN
# -------------------------
USER_IP = f'{st.context.ip_address}'

if "selected_app_key" not in st.session_state:
    st.session_state.selected_app_key = None

c1, c2 = st.sidebar.columns(2)
with c1:
    if st.sidebar.button("🏠 Inicio", use_container_width=True):
        st.session_state.selected_app_key = None
        st.rerun()

# MENÚ
if st.session_state.selected_app_key is None:
    st.sidebar.markdown("---")

    cats = {
        "Fideicomisos y Emisiones": (IA_APPS, "handshake"),
        "Eventos Relevantes": (DS_APPS, "sensors"),
        "Reportes de Emisores": (WS_APPS, "domain"),
        "Calendario Operativo": (RP_APPS, "calendar_month"),
        "Tareas Programadas": (GP_APPS, "menu_book"),
        "Indicadores Económicos": (XX_APPS, "timeline")
    }

    for titulo, (dicc, icono) in cats.items():
        with st.sidebar.expander(titulo, icon=f":material/{icono}:"):
            for name in dicc:
                if st.button(name, key=f"side_{name}", use_container_width=True):
                    st.session_state.selected_app_key = name
                    st.rerun()

# EJECUCIÓN
if st.session_state.selected_app_key:
    app_name = st.session_state.selected_app_key
    archivo_py = TODAS_LAS_APPS.get(app_name)

    if archivo_py:
        try:
            modulo = importlib.import_module(f"app.{archivo_py}")
            importlib.reload(modulo)
            modulo.main()
        except Exception as e:
            st.error(f"Error en módulo {app_name}: {e}")

    gc.collect()
else:
    mostrar_inicio()

# -------------------------
# 🧠 SIDEBAR FOOTER
# -------------------------
st.sidebar.markdown("---")

with st.sidebar.expander("System Status & Support : 🟢", icon=":material/terminal:"):

    st.code(f"""
┌──────────────────────────┐
│  NETWORK CONNECTED [OK]  │
└──────────────────────────┘
 🌐 IP: {USER_IP}
    """, language=None)

    st.status("**Robot-System-IA** | Syncing...", state="running")

    col1, col2 = st.columns(2)
    with col1:
        cpu = random.randint(12, 28)
        st.metric("CPU Load", f"{cpu}%", delta="Normal")
    with col2:
        mem = random.randint(30, 45)
        st.metric("RAM Usage", f"{mem}%", delta="-2%")

    st.progress(cpu)
    st.caption("📡 ROBOT-SYSTEM-IA v1.0 -- TdA.2026")