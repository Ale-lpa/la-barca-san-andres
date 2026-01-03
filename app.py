import streamlit as st
import json

# Configuración de la página
st.set_page_config(page_title="La Barca de San Andrés - Asistente", page_icon="⚓")

# Estilo Elegante Personalizado (Marca Corporativa)
st.markdown("""
    <style>
    .stApp {
        background-color: #F9F7F2;
    }
    .main-header {
        background-color: #002366;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        border-bottom: 4px solid #C5A059;
        margin-bottom: 25px;
    }
    .main-header h1 {
        color: white;
        font-family: 'Playfair Display', serif;
        letter-spacing: 2px;
    }
    .stChatMessage {
        border-radius: 15px;
    }
    </style>
    <div class="main-header">
        <h1>⚓ LA BARCA</h1>
        <p style="color: white; opacity: 0.8; letter-spacing: 3px;">SAN ANDRÉS</p>
    </div>
    """, unsafe_allow_html=True)

# Cargar conocimiento
with open('knowledge.json', 'r', encoding='utf-8') as f:
    knowledge = json.load(f)

# Inicializar historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Bienvenido a bordo! Soy el Capitán de La Barca. 🌊 ¿En qué puedo ayudarle a elegir hoy?"}
    ]

# Mostrar mensajes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Lógica del Chat
if prompt := st.chat_input("Pregúntame por el pescado del día..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respuesta lógica del "Capitán"
    with st.chat_message("assistant"):
        response = f"¡Excelente pregunta! Como Capitán de esta casa, le informo que nuestro {knowledge['menu']['pescados_frescos']}. Si busca algo especial, le recomiendo nuestras {knowledge['menu']['platos_estrella'][0]} maridadas con un {knowledge['menu']['bodega'][0]}."
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
