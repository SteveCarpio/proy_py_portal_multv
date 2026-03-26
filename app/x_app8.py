# 📂 Gestor de Proyectos
import streamlit as st

def main() -> None:
    import sqlite3
    import pandas as pd
    from datetime import datetime
    import io
    from typing import List, Tuple, Any, Optional

    DB_PATH = "data/app8_proyectos.db"
    # --- GESTIÓN DE BASE DE DATOS (SQLite) ---

    def init_db() -> None:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Tabla Usuarios
        c.execute('''CREATE TABLE IF NOT EXISTS users 
                    (username TEXT PRIMARY KEY, password TEXT, role TEXT)''')
        
        # Tabla Proyectos
        c.execute('''CREATE TABLE IF NOT EXISTS projects 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    name TEXT, 
                    developer TEXT, 
                    created_at TEXT,
                    status_global TEXT DEFAULT 'Pendiente')''')
        
        # Tabla Fases
        c.execute('''CREATE TABLE IF NOT EXISTS phases 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    project_id INTEGER, 
                    name TEXT, 
                    description TEXT, 
                    status TEXT, 
                    dev_notes TEXT,
                    FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE)''')
        
        # Tabla Notas del Supervisor
        c.execute('''CREATE TABLE IF NOT EXISTS supervisor_notes 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    project_id INTEGER, 
                    note TEXT, 
                    created_at TEXT,
                    FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE)''')

        # Insertar usuarios por defecto si no existen
        c.execute("SELECT * FROM users WHERE username = 'admin'")
        if not c.fetchone():
            users = [
                ('admin', 'admin123', 'Supervisor'),
                ('SteveCarpio', 'dev123', 'Desarrollador'),
                ('LuisRomero', 'dev123', 'Desarrollador')
            ]
            c.executemany("INSERT INTO users VALUES (?,?,?)", users)
        
        conn.commit()
        conn.close()

    # Función SOLO para escribir (Insert, Update, Delete) -> No devuelve datos
    def run_action(query: str, params: tuple = ()) -> None:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(query, params)
        conn.commit()
        conn.close()

    # Función SOLO para leer (Select) -> Siempre devuelve una lista
    def run_select(query: str, params: tuple = ()) -> List[Tuple[Any, ...]]:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(query, params)
        data = c.fetchall()
        conn.close()
        return data

    def get_data_as_df(query: str, params: tuple = ()) -> pd.DataFrame:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df

    # --- FUNCIONES DE ESTILO Y UTILIDAD ---

    def get_color(status: str) -> Tuple[str, str]:
        if status == 'En curso':
            return '#d4edda', 'green' # Fondo verde claro, texto verde
        elif status == 'Pendiente':
            return '#fff3cd', 'orange' # Fondo naranja claro, texto naranja
        elif status == 'Finalizado':
            return '#e2e3e5', 'gray' # Fondo gris, texto gris
        return '#ffffff', 'black'

    # --- INTERFAZ: LOGIN ---

    def login() -> None:
        st.markdown("<h1 style='text-align: center;'>🔐 Acceso al Gestor</h1>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            with st.form("login_form"):
                username = st.text_input("Usuario")
                password = st.text_input("Contraseña", type="password")
                submit = st.form_submit_button("Entrar")
                
                if submit:
                    # Usamos run_select que garantiza devolver una lista
                    user_data = run_select("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
                    if user_data:
                        # user_data es una lista de tuplas, tomamos el primer elemento
                        user = user_data[0] 
                        st.session_state['logged_in'] = True
                        st.session_state['username'] = user[0]
                        st.session_state['role'] = user[2]
                        st.rerun()
                    else:
                        st.error("Usuario o contraseña incorrectos")

    # --- INTERFAZ: SIDEBAR ---

    st.sidebar.subheader("📂 Gestor de Proyectos")
    st.sidebar.caption("- Desarrollo de VBA y PYTHON") #  👉

    def sidebar_menu() -> Tuple[str, str]:
        # Verificar tipos para Pylance antes de mostrar
        current_user = str(st.session_state.get('username', 'Usuario'))
        current_role = str(st.session_state.get('role', 'Rol'))

        st.sidebar.title(f"👤 {current_user}")
        st.sidebar.caption(f"Rol: {current_role}")
        st.sidebar.markdown("---")
        
        selected_dev = "Todos"
        selected_status = "Todos"

        if current_role == 'Supervisor':
            st.sidebar.header("🔍 Filtros")
            # run_select devuelve lista, así que la comprensión de lista es segura
            raw_devs = run_select("SELECT DISTINCT username FROM users WHERE role='Desarrollador'")
            devs = [x[0] for x in raw_devs] # Pylance ahora sabe que raw_devs es iterable
            
            selected_dev = st.sidebar.selectbox("Filtrar por Desarrollador", ["Todos"] + devs)
            selected_status = st.sidebar.selectbox("Filtrar por Estado", ["Todos", "En curso", "Pendiente", "Finalizado"])
            
            st.sidebar.markdown("---")
            
            if st.sidebar.button("📥 Exportar Reporte Excel"):
                df_proyectos = get_data_as_df("SELECT * FROM projects")
                df_fases = get_data_as_df("SELECT * FROM phases")
                
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    df_proyectos.to_excel(writer, sheet_name='Proyectos', index=False)
                    df_fases.to_excel(writer, sheet_name='Fases_Detalle', index=False)
                    
                st.sidebar.download_button(
                    label="Descargar Excel",
                    data=buffer,
                    file_name="reporte_proyectos.xlsx",
                    mime="application/vnd.ms-excel"
                )

        #st.sidebar.markdown("---")
        if st.sidebar.button("🚪 Cerrar Sesión"):
            st.session_state['logged_in'] = False
            st.rerun()
        #st.sidebar.markdown("---")
            
        return selected_dev, selected_status

    # --- VISTA: SUPERVISOR ---

    def supervisor_view(filter_dev: str, filter_status: str) -> None:
        st.subheader("📊 Supervisión de Proyectos")
        
        query = "SELECT * FROM projects WHERE 1=1"
        params: List[Any] = []
        
        if filter_dev != "Todos":
            query += " AND developer = ?"
            params.append(filter_dev)
        
        if filter_status != "Todos":
            query += " AND status_global = ?"
            params.append(filter_status)
            
        # run_select siempre retorna lista, len() funciona seguro
        projects = run_select(query, tuple(params))
        
        total = len(projects)
        # Accedemos a indices seguros porque projects es List[Tuple]
        en_curso = len([p for p in projects if p[4] == 'En curso'])
        pendientes = len([p for p in projects if p[4] == 'Pendiente'])
        finalizados = len([p for p in projects if p[4] == 'Finalizado'])
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Proyectos", total)
        m2.metric("En Curso", en_curso, delta_color="normal")
        m3.metric("Pendientes", pendientes, delta_color="off")
        m4.metric("Finalizados", finalizados)
        
        st.markdown("---")

        tab_vivos, tab_hist = st.tabs(["🔥 Proyectos Vivos", "🏁 Histórico Finalizado"])
        
        def render_project_card(proj: Tuple[Any, ...]) -> None:
            pid, pname, pdev, pdate, pstatus = proj
            
            bg_color, text_color = get_color(str(pstatus))
            
            with st.container():
                st.markdown(f"""
                <div style='background-color: {bg_color}; padding: 10px; border-radius: 10px 10px 0 0; border: 1px solid #ddd;'>
                    <h3 style='color: {text_color}; margin:0;'>{pname}</h3>
                    <small>Dev: <b>{pdev}</b> | Creado: {pdate}</small>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("Ver Fases y Notas", expanded=False):
                    phases = run_select("SELECT * FROM phases WHERE project_id = ?", (pid,))
                    if phases:
                        st.markdown("##### Fases del Proyecto")
                        for ph in phases:
                            ph_status = ph[4]
                            c_bg, c_tx = get_color(str(ph_status))
                            st.markdown(f"""
                            <div style='border-left: 5px solid {c_tx}; padding-left: 10px; margin-bottom: 5px;'>
                                <b>{ph[2]}</b> <span style='background-color:{c_bg}; color:{c_tx}; padding:2px 6px; border-radius:4px; font-size:0.8em;'>{ph_status}</span><br>
                                <i>{ph[3]}</i>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("No hay fases definidas aún.")
                    
                    st.markdown("---")
                    st.write("**📝 Notas de Supervisión:**")
                    
                    old_notes = run_select("SELECT note, created_at FROM supervisor_notes WHERE project_id = ?", (pid,))
                    for note in old_notes:
                        st.text(f"[{note[1]}] {note[0]}")
                    
                    new_note = st.text_input(f"Añadir nota para {pname}", key=f"note_{pid}")
                    if st.button("Guardar Nota", key=f"btn_note_{pid}"):
                        if new_note:
                            run_action("INSERT INTO supervisor_notes (project_id, note, created_at) VALUES (?, ?, ?)", 
                                    (pid, new_note, datetime.now().strftime("%Y-%m-%d %H:%M")))
                            st.success("Nota guardada")
                            st.rerun()

        with tab_vivos:
            for p in projects:
                if p[4] != 'Finalizado':
                    render_project_card(p)
                    st.write("") 

        with tab_hist:
            for p in projects:
                if p[4] == 'Finalizado':
                    render_project_card(p)
                    st.write("")

    # --- VISTA: DESARROLLADOR ---

    def developer_view() -> None:
        current_username = str(st.session_state.get('username'))
        st.subheader(f"👨‍💻 Espacio de trabajo: {current_username}")
        
        with st.expander("➕ Crear Nuevo Proyecto", expanded=False):
            with st.form("new_project"):
                proj_name = st.text_input("Nombre del Proyecto")
                submitted = st.form_submit_button("Crear Proyecto")
                if submitted and proj_name:
                    run_action("INSERT INTO projects (name, developer, created_at, status_global) VALUES (?, ?, ?, ?)",
                            (proj_name, current_username, datetime.now().strftime("%Y-%m-%d"), 'Pendiente'))
                    st.success("Proyecto Creado")
                    st.rerun()

        #st.markdown("---")
        
        my_projects = run_select("SELECT * FROM projects WHERE developer = ?", (current_username,))
        
        if not my_projects:
            st.info("No tienes proyectos activos.")
            return

        tab_active, tab_finished = st.tabs(["En Desarrollo", "Finalizados"])

        
        st.sidebar.markdown(f"### Listado de Proyectos")
        def render_dev_project(proj: Tuple[Any, ...]) -> None:
            pid, pname, pdev, pdate, pstatus = proj
            
            
            
            st.markdown(f"#### 📂 {pname}")
            
            col_stat, col_del = st.columns([1, 3])
            with col_del:
                st.write("Creado")
                st.caption(" " + pdate)
            with col_stat:
                options = ["Pendiente", "En curso", "Finalizado"]
                try:
                    idx = options.index(pstatus)
                except ValueError:
                    idx = 0
                
                new_status_global = st.selectbox("Estado Global del Proyecto", 
                                                options, 
                                                index=idx,
                                                key=f"g_stat_{pid}")
                if new_status_global != pstatus:
                    run_action("UPDATE projects SET status_global = ? WHERE id = ?", (new_status_global, pid))
                    st.rerun()


            #st.sidebar.markdown(f"{pname} ({pstatus})") #  📂



            bg_color, text_color = get_color(str(pstatus))
            
            
            #st.sidebar.markdown(f"""
            #    <div style='background-color: {bg_color}; padding: 10px; border-radius: 10px 10px 0 0; border: 1px solid #ddd;'>
            #        <h3 style='color: {text_color}; margin:0;'>{pname}</h3>
            #        <small>Dev: <b>{pdev}</b> | Creado: {pdate}</small>
            #    </div>
            #    """, unsafe_allow_html=True)

            st.sidebar.markdown(f"""
                <div style='background-color: {bg_color}; padding: 1px; border-radius: 5px 5px 0 0; border: 1px solid #ddd;'>
                    <h4 style='color: {text_color}; margin:0;'> - {pname}</h4>
                </div>
                """, unsafe_allow_html=True)



            #st.markdown("**Gestión de Fases**")
            with st.expander(f"Configuración del proyecto ", expanded=False):
            
                phases = run_select("SELECT * FROM phases WHERE project_id = ?", (pid,))
                
                for ph in phases:
                    ph_id, _, ph_name, ph_desc, ph_status, ph_notes = ph
                    
                    with st.expander(f"📍 {ph_name} ({ph_status})"):
                        with st.form(f"edit_phase_{ph_id}"):
                            e_name = st.text_input("Nombre Fase", value=ph_name)
                            e_desc = st.text_area("Descripción", value=ph_desc)
                            
                            p_opts = ["Pendiente", "En curso", "Finalizado"]
                            try: 
                                p_idx = p_opts.index(ph_status) 
                            except ValueError: 
                                p_idx = 0
                                
                            e_stat = st.selectbox("Estado", p_opts, index=p_idx)
                            e_note = st.text_area("Notas Técnicas", value=ph_notes)
                            
                            c1, c2 = st.columns(2)
                            with c1:
                                if st.form_submit_button("💾 Actualizar Fase"):
                                    run_action("""UPDATE phases SET name=?, description=?, status=?, dev_notes=? 
                                                WHERE id=?""", (e_name, e_desc, e_stat, e_note, ph_id))
                                    st.rerun()
                            with c2:
                                delete_check = st.checkbox("Borrar esta fase", key=f"del_chk_{ph_id}")
                                if delete_check and st.form_submit_button("Confirmar Borrado"):
                                    run_action("DELETE FROM phases WHERE id=?", (ph_id,))
                                    st.rerun()

                with st.expander("➕ Añadir Nueva Fase", expanded=False):
                    with st.form(f"add_phase_{pid}"):
                        n_name = st.text_input("Nombre de la Fase (Ej: Fase 1)")
                        n_desc = st.text_area("Descripción")
                        n_stat = st.selectbox("Estado Inicial", ["Pendiente", "En curso", "Finalizado"])
                        n_note = st.text_area("Notas Técnicas (Opcional)")
                        
                        if st.form_submit_button("Añadir Fase"):
                            run_action("INSERT INTO phases (project_id, name, description, status, dev_notes) VALUES (?,?,?,?,?)",
                                    (pid, n_name, n_desc, n_stat, n_note))
                            st.rerun()

                sup_notes = run_select("SELECT note, created_at FROM supervisor_notes WHERE project_id = ?", (pid,))
                if sup_notes:
                    st.warning("👁️ Notas del Supervisor:")
                    for sn in sup_notes:
                        st.caption(f"{sn[1]}: {sn[0]}")
                
                with st.expander(f"🗑️ Eliminar Proyecto ", expanded=False):
                        st.caption("Precaución borrará todo rastro del proyecto.")
                        if st.button("¿Estás seguro?", key=f"del_{pid}", type="primary"):
                            run_action("DELETE FROM projects WHERE id = ?", (pid,))
                            st.rerun()
                            #st.toast("Funcionalidad de borrado deshabilitada temporalmente, quiero poner una Re-Confirmación.")

            #st.divider()

        with tab_active:
            for p in my_projects:
                if p[4] != 'Finalizado':
                    render_dev_project(p)
                    
        with tab_finished:
            for p in my_projects:
                if p[4] == 'Finalizado':
                    render_dev_project(p)

    # --- MAIN APP FLOW ---


    init_db()
    
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        
    if not st.session_state['logged_in']:
        login()
    else:
        filter_dev, filter_status = sidebar_menu()
        
        current_role = st.session_state.get('role')
        if current_role == 'Supervisor':
            supervisor_view(filter_dev, filter_status)
        else:
            developer_view()

if __name__ == "__main__":
    main()