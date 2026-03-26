import streamlit as st

# ----------------------------------------
# EJECUCIÓN PRINCIPAL
# ----------------------------------------
def main():
    st.title("🚧 En construcción 🚧")
    st.subheader(""" 
    🏛️ Fideicomisos y Emisiones

Comportamiento:

Selector de emisor/fideicomiso
Submenú dinámico:

Subsecciones:

📄 Documentación
👥 Asambleas de Tenedores
📊 Reportes
📎 Otros Documentos
🚨 Eventos Relevantes (solo de ese fideicomiso)   
    """)

    st.sidebar.write("Aquí un SELECTBOX de Emisores")


if __name__ == "__main__":
    main()
