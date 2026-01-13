import streamlit as st
import json

# 1. CONFIGURACIÓN DE PÁGINA Y ESTÉTICA
st.set_page_config(page_title="La Barca de San Andrés", page_icon="⚓")

# Estilo CSS para arreglar el nombre y el diseño
st.markdown("""
    <style>
    .titulo-contenedor {
        text-align: left;
        line-height: 0.8;
        margin-bottom: 20px;
    }
    .linea1 {
        font-family: 'serif';
        font-size: 42px;
        font-weight: bold;
        color: #002344;
    }
    .linea2 {
        font-family: 'serif';
        font-size: 42px;
        font-weight: bold;
        color: #002344;
        margin-top: 10px;
    }
    .subtitulo {
        font-size: 18px;
        letter-spacing: 4px;
        color: #002344;
        border-top: 2px solid #002344;
        padding-top: 5px;
        display: inline-block;
        margin-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. ENCABEZADO (Corrección de espacio en el nombre)
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("""
        <div class="titulo-contenedor">
            <div class="linea1">La Barca de</div>
            <div class="linea2">San Andrés</div>
            <div class="subtitulo">DESDE 1980</div>
        </div>
        """, unsafe_allow_html=True)
with col2:
    st.image("logo_timon.png", width=120) # Asegúrate de tener el logo en el directorio

st.divider()

# 3. LÓGICA DEL ASISTENTE (System Prompt Integrado)
# El prompt interno obliga a la IA a dar precio y maridaje siempre.
SYSTEM_PROMPT = """
Eres el Maître virtual de La Barca de San Andrés. 
REGLA CRÍTICA: Cada vez que un usuario pregunte por comida, debes responder:
1. Nombre del plato y su PRECIO exacto.
2. Una RECOMENDACIÓN DE MARIDAJE de nuestra bodega (según el JSON).
Responde en el idioma del cliente de forma directa y elegante. No uses guiones de bienvenida largos.
"""

# 4. CHAT INTERFACE
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial de chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de usuario
if prompt := st.chat_input("Hable con el capitán..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Aquí se integraría la llamada a la API (Gemini/OpenAI) 
        # enviando el SYSTEM_PROMPT + el contenido del JSON.
        response = "Ejemplo de respuesta: Nuestras Lapas a la Carmela (10,50€) son excelentes. Le recomiendo maridarlas con un Yaiza Seco (28,50€) para resaltar su frescura volcánica."
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# Pie de página
st.sidebar.markdown("---")
st.sidebar.write("🔒 Administración de la aplicación")
