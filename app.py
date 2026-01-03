import streamlit as st
import json

# Configuración de la página
st.set_page_config(page_title="La Barca de San Andrés - Capitán Virtual", page_icon="⚓", layout="centered")

# --- ESTILO VISUAL PREMIUM (CSS) ---
# Inspirado en la tarjeta de visita: fondo oscuro, luces cálidas, madera, dorado y azul marino.
st.markdown("""
    <style>
    /* 1. Fondo de la App (Estilo Taberna Cálida) */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url('https://i.imgur.com/Q2Q9Z4O.jpg'); /* Imagen de fondo estilo bodega/luces bokeh */
        background-size: cover;
        background-position: center;
        color: #EAEAEA; /* Texto general claro */
        font-family: 'Georgia', serif;
    }

    /* 2. Cabecera con Logo de Ancla y Pescado */
    .header-container {
        text-align: center;
        padding: 40px 20px 20px;
        background: rgba(0, 35, 102, 0.85); /* Azul marino translúcido */
        border-bottom: 4px solid #D4AF37; /* Dorado */
        border-radius: 0 0 25px 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin-bottom: 30px;
    }
    .logo-img {
        font-size: 4rem;
        color: #D4AF37; /* Ancla dorada */
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .header-container h1 {
        font-family: 'Playfair Display', serif;
        letter-spacing: 4px;
        color: #D4AF37; /* Dorado */
        margin: 0;
        text-transform: uppercase;
        font-size: 2rem;
    }
    .header-container p {
        font-size: 0.9rem;
        letter-spacing: 5px;
        color: #EAEAEA;
        opacity: 0.8;
        margin-top: 5px;
        text-transform: uppercase;
    }

    /* 3. Estilo de las Burbujas de Chat */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.1) !important; /* Fondo translúcido para el contenedor */
        border: none !important;
        padding: 10px !important;
    }
    
    /* Burbuja del Asistente (Capitán) */
    .stChatMessage[data-testid="stChatMessage"] > div:nth-child(1) {
        background-color: #002366; /* Azul Marino */
        border: 2px solid #D4AF37; /* Borde Dorado */
        color: #EAEAEA;
    }
    
    /* Burbuja del Usuario */
    .stChatMessage[data-testid="stChatMessage"] > div:nth-child(3) {
        background-color: rgba(212, 175, 55, 0.8); /* Dorado translúcido */
        color: #1A1A1A; /* Texto oscuro */
        font-weight: 500;
    }

    /* 4. Input de Texto */
    .stChatInput > div {
        background-color: rgba(255,255,255,0.15) !important;
        border: 2px solid #D4AF37 !important;
        color: white !important;
    }
    .stChatInput input { color: white !important; }

    /* 5. Footer de Marca */
    .branding-footer {
        text-align: center;
        font-size: 0.75rem;
        color: rgba(255,255,255,0.6);
        padding: 25px 0;
        margin-top: auto;
    }
    .branding-footer b { color: #D4AF37; }
    </style>

    <div class="header-container">
        <div class="logo-img">⚓🐟</div> <h1>LA BARCA</h1>
        <p>San Andrés</p>
    </div>
    """, unsafe_allow_html=True)

# Cargar el cerebro
try:
    with open('knowledge.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    st.error("Error: No se encontró el archivo 'knowledge.json'. Asegúrate de subirlo a GitHub.")
    st.stop()

# Inicializar historial de chat con el Ancla como avatar
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": f"¡Saludos, grumete! Soy el **Capitán de La Barca**. ⚓ Hoy la mar nos ha traído un género espectacular. ¿Le apetece probar nuestra especialidad, el **{data['sugerencia_dia']}**?", "avatar": "⚓"}
    ]

# Mostrar mensajes
for message in st.session_state.messages:
    # Usamos el avatar personalizado si existe, si no, el por defecto
    avatar_icon = message.get("avatar")
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

# Lógica del Chat (Simulada para la Demo Visual)
if prompt := st.chat_input("Pregunte al Capitán por el pescado del día..."):
    # Mensaje del usuario (con avatar de persona si quieres, o default)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respuesta del Asistente (Capitán con Ancla)
    with st.chat_message("assistant", avatar="⚓"):
        # Aquí iría la llamada real a tu IA. Esta es una respuesta de ejemplo usando el JSON.
        response_text = f"¡A la orden! Para un paladar exigente, no hay nada mejor que nuestro **{data['menu']['platos_principales'][0]['plato']}** ({data['menu']['platos_principales'][0]['precio']}). Le aseguro que maridado con un **{data['menu']['bodega'][0]['nombre']}** es una experiencia de otro nivel. ¿Se lo voy marchando?"
        st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text, "avatar": "⚓"})

# Footer
st.markdown("<div class='branding-footer'>Diseñado a medida por <b>LocalMind AI</b> para La Barca de San Andrés.</div>", unsafe_allow_html=True)
