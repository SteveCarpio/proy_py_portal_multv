import streamlit as st
import gc
import base64
import random
import importlib
import subprocess
from datetime import datetime
from PIL import Image

# 1. CONFIGURACIÓN DE PÁGINA (ESTILO FINANCIERO).
st.set_page_config(
    page_title="Portal TDA: [ MULTIVA ]",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. ESTILOS CSS PERSONALIZADOS (UI/UX)
st.markdown("""
    <style>
    /* Estilo para las 'Cards' de las aplicaciones */
    .app-card {
        background-color: #f8f9fa;
        border-left: 5px solid #1c2e4a;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        transition: transform 0.2s;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    .app-card:hover {
        transform: translateY(-5px);
        box-shadow: 2px 5px 15px rgba(0,0,0,0.1);
    }
    .fin-header {
        color: #1c2e4a;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 700;
        border-bottom: 2px solid #e9ecef;
        padding-bottom: 10px;
        margin-top: 20px;
    }
    .small-text-fin {
        font-size: 0.85rem;
        color: #555;
        line-height: 1.4;
    }
    .tag-ia { color: #FF6200; font-weight: bold; font-size: 0.7rem; text-transform: uppercase; }
    
    .tag-titulo-tda { color: #555; font-size: 0.7rem; }
    
    .tag-titulo-user-ok { color: #668555; font-size: 0.7rem; }
    .tag-titulo-user-ko { color: #FF6200; font-size: 0.7rem; }
    /* Ajustes en el Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. DICCIONARIOS DE APLICACIONES (LÓGICA INTERNA)
IA_APPS = {
    "   Emisores": "app1"
   
}
DS_APPS = {
    "Listado Historico": "app2"

}
WS_APPS = {
    "Trimestrales": "app3"
  
}
RP_APPS = {
    "Publicaciones": "app4",
    "Festivos": "app5",  
  
}
GP_APPS = {"Semanales / Mensuales   ": "app6"}

XX_APPS = {"Bolsa-MX": "app7",
           "Global": "app8"
           }


TODAS_LAS_APPS = {**IA_APPS, **DS_APPS, **WS_APPS, **RP_APPS, **GP_APPS, **XX_APPS}


def get_image_base64(path):
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except: return ""

def mostrar_inicio():
    # HEADER CON LOGO
    COL_ANCHO = 0.5

    col_t1, col_t2, col_t3 = st.columns([3, COL_ANCHO ,1])
    with col_t1:
        st.caption("""
                   -----------------------------------------------------------------

                   📢 [Ticker Noticias / Indicadores] .............23234.......56456456.......rfg_34535........................

                   -----------------------------------------------------------------
                   """)
        
        #st.markdown(f'<p class="tag-titulo-tda">⬅️ Seleccione una herramienta en el panel izquierdo para comenzar.</p>', unsafe_allow_html=True)
        
    with col_t3:
        try:
            logo = Image.open("img/logo_multiva2.png")
            st.image(logo)  # , width=150
            
        except: pass

    #st.markdown("Bienvenido al portal analítico. Seleccione una herramienta en el panel izquierdo para comenzar.")
    #st.markdown('<p class="tag-titulo-tda">Bienvenido al portal analítico. Seleccione una herramienta en el panel izquierdo para comenzar.</p>', unsafe_allow_html=True)

    # --- 🏛️ Fideicomisos y Emisiones ---
    st.markdown('<h3 class="fin-header">🏛️ Fideicomisos y Emisiones</h3>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="app-card"><h4>Emisores</h4><p class="tag-ia">Shared Folder</p><p class="small-text-fin">Datos de Documentos, etc, etc... etc.....</p></div>', unsafe_allow_html=True)
        pass
    with c2:
        #st.markdown('<div class="app-card"><h4>Transcripción</h4><p class="tag-ia">Audio Intelligence</p><p class="small-text-fin">Conversión de voz a texto y generación automática de minutas.</p></div>', unsafe_allow_html=True)
        pass
    with c3:
        #st.markdown('<div class="app-card"><h4>ChatTDA</h4><p class="tag-ia">Assistant</p><p class="small-text-fin">Interfaz conversacional inteligente con soporte para documentos internos.</p></div>', unsafe_allow_html=True)
        pass

    # --- 🚨 Eventos Relevantes ---
    st.markdown('<h3 class="fin-header">🚨 Eventos Relevantes</h3>', unsafe_allow_html=True)
    cd1, cd2, cd3 = st.columns(3)
    with cd1:
        st.markdown('<div class="app-card"><h4>xxxxx</h4><p class="tag-ia">xxxxx</p><p class="small-text-fin">xxxxxxxxxxxx.</p></div>', unsafe_allow_html=True)
    with cd2:
        #st.markdown('<div class="app-card"><h4>Flujos Bloomberg</h4> <p class="tag-ia">Treasury Operations</p>  <p class="small-text-fin">Procesamiento y conversión de flujos de inversión para la integración directa con terminales Bloomberg.</p></div>', unsafe_allow_html=True)
        pass
    with cd3:
        pass
        #st.markdown('<div class="app-card"><h4>Entidades Financieras</h4> <p class="tag-ia">Official Historical Registry</p> <p class="small-text-fin">Visualización y seguimiento histórico de las Entidades Financieras registradas en el Banco de España. </p></div>', unsafe_allow_html=True)

    # --- 📑 Reportes de Emisores ---
    st.markdown('<h3 class="fin-header">📑 Reportes de Emisores</h3>', unsafe_allow_html=True)
    cw1, cw2, cw3 = st.columns(3)
    with cw1:
        st.markdown('<div class="app-card"><h4>xxxxx</h4><p class="tag-ia">xxxxx</p><p class="small-text-fin">xxxxxxxxxxxx.</p></div>', unsafe_allow_html=True)                                                                                                                                         
    with cw2:
        #st.markdown('<div class="app-card"><h4>Estados Financieros</h4> <p class="tag-ia">Data Extraction</p>  <p class="small-text-fin">Extracción bajo demanda de reportes financieros oficiales desde el repositorio de la CNBV.</p></div>', unsafe_allow_html=True)
        pass    
    # --- 📅 Calendario Operativo ---
    st.markdown('<h3 class="fin-header">📅 Calendario Operativo</h3>', unsafe_allow_html=True)
    cr1, cr2, cr3 = st.columns(3)
    with cr1:
        st.markdown('<div class="app-card"><h4>Publicaciones</h4> <p class="tag-ia">xxxxxx</p> <p class="small-text-fin">xxxxxxxxx. </p></div>', unsafe_allow_html=True)
    with cr2:
        st.markdown('<div class="app-card"><h4>Festivos</h4> <p class="tag-ia">xxxxxxxx</p>  <p class="small-text-fin">xxxxxxxxxxxxxxx.</p></div>', unsafe_allow_html=True) 
    with cr3:
        pass
        #st.markdown('<div class="app-card"><h4>Analizador Financiero</h4> <p class="tag-ia">Banxico & Yahoo Finance API</p>  <p class="small-text-fin">Extracción y visualización de indicadores económicos y bursátiles históricos para análisis corporativo.</p></div>', unsafe_allow_html=True)


    # --- ✅ Tareas Programadas ---
    st.markdown('<h3 class="fin-header">✅ Tareas Programadas</h3>', unsafe_allow_html=True)
    cw1, cw2, cw3 = st.columns(3)
    with cw1:
        st.markdown('<div class="app-card"><h4>xxxxx</h4><p class="tag-ia">xxxxx</p><p class="small-text-fin">xxxxxxxxxxxx.</p></div>', unsafe_allow_html=True)                                                                                                                                         
    

    # --- 📊 Indicadores Económicos ---
    st.markdown('<h3 class="fin-header">📊 Indicadores Económicos</h3>', unsafe_allow_html=True)
    cw1, cw2, cw3 = st.columns(3)
    with cw1:
        st.markdown('<div class="app-card"><h4>xxxxx</h4><p class="tag-ia">xxxxx</p><p class="small-text-fin">xxxxxxxxxxxx.</p></div>', unsafe_allow_html=True)                                                                                                                                         
    


    # --- FOOTER ---
    st.markdown("---")
    img_b64 = get_image_base64("img/logotipo.ico")     
    if img_b64:
        st.markdown(f"<div style='text-align: center;'><img src='data:image/png;base64,{img_b64}' width='30'><br><small>© {datetime.now().year} Titulización de Activos S.A. - Confidencial</small></div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------

# 5. LÓGICA DE NAVEGACIÓN (CON CARGA DINÁMICA)

# Carga de datgos de conexión
USER_IP = f'{st.context.ip_address}'


if "selected_app_key" not in st.session_state:
    st.session_state.selected_app_key = None

# Sidebar Superior
#st.sidebar.markdown("### Navegación")

c_side1, c_side2 = st.sidebar.columns(2)
with c_side1:
    if st.sidebar.button("🏠 Inicio", width='stretch'):
        st.session_state.selected_app_key = None
        st.rerun()
    
with c_side2:
    pass
    

# Menú Lateral
if st.session_state.selected_app_key is None:
    st.sidebar.markdown("---")
    # https://fonts.google.com/icons?utm_source=chatgpt.com&icon.size=24&icon.color=%238B1A10&icon.set=Material+Icons&selected=Material+Icons+Outlined:build:
    cats = {
        "Fideicomisos y Emisiones": (IA_APPS, "handshake"),          # handshake o account_balance
        "Eventos Relevantes": (DS_APPS, "sensors"),                  # sensors o radar
        "Reportes de Emisores": (WS_APPS, "domain"),                 # domain o corporate_fare
        "Calendario Operativo": (RP_APPS, "calendar_month"),      # 
        "Tareas Programadas": (GP_APPS, "menu_book"),            # menu_book o info
        "Indicadores Económicos ": (XX_APPS, "timeline")        # timeline o line_axis
    }
    
    for titulo, (dicc, icono) in cats.items():
        with st.sidebar.expander(titulo, icon=f":material/{icono}:"):
            for name in dicc:
                if st.button(name, key=f"side_{name}", width='stretch'):
                    st.session_state.selected_app_key = name
                    st.rerun()

# EJECUCIÓN DINÁMICA
if st.session_state.selected_app_key:
    app_name = st.session_state.selected_app_key
    archivo_py = TODAS_LAS_APPS.get(app_name)
    
    if archivo_py:
        # Botón para volver atrás visible mientras se usa la app
        #if st.sidebar.button("⬅️ Salir de la App", type="primary"):
        #    st.session_state.selected_app_key = None
        #    st.rerun()
            
        try:
            modulo = importlib.import_module(f"app.{archivo_py}")
            importlib.reload(modulo)
            modulo.main()
        except Exception as e:
            st.error(f"Error en módulo {app_name}: {e}")
    gc.collect()
else:
    mostrar_inicio()

st.sidebar.markdown("---")


# --- PIE DE PAGINA DEL SIDEBAR ---
with st.sidebar.expander("System Status & Support : 🟢", icon=":material/terminal:", expanded=False): 
    
    st.code(f"""
┌──────────────────────────┐
│  NETWORK CONNECTED [OK]  │
└──────────────────────────┘
 🌐 IP: {USER_IP}
    
───────────────────────────
 🆘 HELP: xxxx@tda-sgft.com
───────────────────────────
    
    ⚙️ INFRASTRUCTURE:
 🐍 PyCore: 3.12
 🐧 Kernel: Linux 6.17
 🚀 App   : Streamlit 
 📊 Data  : Pandas 2.3
    """, language=None)

    st.status("**Robot-System-IA** | Syncing...", state="running", )

    
    # 3. Métricas de Rendimiento (Simuladas para el efecto visual)
    col1, col2 = st.columns(2)
    with col1:
        cpu_sim = random.randint(12, 28)
        st.metric("CPU Load", f"{cpu_sim}%", delta="Normal")
    with col2:
        mem_sim = random.randint(30, 45)
        st.metric("RAM Usage", f"{mem_sim}%", delta="-2%")

    st.progress(cpu_sim, text="System Stability")
       
    # 1. Un toque artístico con ASCII Art minimalista
    st.caption("📡 𝚁𝙾𝙱𝙾𝚃-𝚂𝚈𝚂𝚃𝙴𝙼-𝙸𝙰 𝚟𝟷.𝟶 -- TdA.2026")
    


# ICONOS:
# 📡⚡ 🟢  

# MATERIAL:
# :material/info:
