import streamlit as st
import json

# Configuración de la página
st.set_page_config(page_title="La Barca de San Andrés - Capitán", page_icon="⚓", layout="centered")

# --- CUSTOM CSS: ESTILO TARJETA DE VISITA ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Poppins:wght@300;400&display=swap');

    /* 1. Fondo General (Oscuro y Elegante como la tarjeta) */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                    url('https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?q=80&w=2070&auto=format&fit=crop'); 
        background-size: cover;
        background-attachment: fixed;
    }

    /* 2. Cabecera Estilo Logo (Ancla + Pescado) */
    .header-container {
        text-align: center;
        padding: 50px 20px;
        border-bottom: 2px solid #C5A059;
        margin-bottom: 30px;
    }
    .nautical-logo {
        font-size: 50px;
        color: #C5A059;
        margin-bottom: 10px;
        filter: drop-shadow(0px 4px 4px rgba(0,0,0,0.5));
    }
    .header-container h1 {
        font-family: 'Playfair Display', serif;
        color: #C5A059;
        font-size: 2.8rem;
        letter-spacing: 6px;
        margin: 0;
        text-transform: uppercase;
    }
    .header-container p {
        font-family: 'Poppins', sans-serif;
        color: white;
        letter-spacing: 8px;
        font-size: 0.8rem;
        text-transform: uppercase;
        opacity: 0.7;
    }

    /* 3. QUITAR EL CUADRO DEL ROBOT Y ESTILO DE MENSAJES */
    /* Quitamos el fondo gris por defecto de Streamlit */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
    }

    /* Estilo para el mensaje del CAPITÁN (Ancla) */
    .bot-bubble {
        background: rgba(0, 35, 102, 0.7); /* Azul Marino */
        border-left: 5px solid #C5A059;
        padding: 20px;
        border-radius: 0px 20px 20px 20px;
        color: white;
        font-family: 'Poppins', sans-serif;
        box-shadow: 10px 10px 20px rgba(0,0,0,0.3);
    }

    /* Estilo para el mensaje del CLIENTE */
    .user-bubble {
        background: rgba(197, 160, 89, 0.2); /* Dorado muy suave */
        border-right: 5px solid #C5A059;
        padding: 15px;
        border-radius: 20px 0px 20px 20px;
        color: #C5A059;
        text-align: right;
        font-family: 'Poppins', sans-serif;
        margin-left: 20%;
    }

    /* 4. Input de Texto (Elegante) */
    .stChatInput {
        padding-bottom: 30px;
    }
    .stChatInput div {
        background-color: rgba(255,255,255,0.05) !important;
        border: 1px solid #C5A059 !important;
        border-radius: 50px !important;
    }
    
    /* Ocultar avatares por defecto de Streamlit */
    [data-testid="stChatMessageAvatarAssistant"], [data-testid="stChatMessageAvatarUser"] {
        display: none !important;
    }

    </style>
    
    <div class="header-container">
        <div class="nautical-logo">⚓ 🐟</div>
        <h1>LA BARCA</h1>
        <p>SAN ANDRÉS</p>
    </div>
    """, unsafe_allow_html=True)

# --- LÓGICA DE DATOS ---
try:
    with open('knowledge.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except:
    st.error("Por favor, sube el archivo knowledge.json")
    st.stop()

# Inicializar historial
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Saludos! Soy el Capitán de La Barca. ⚓ Hoy el mar nos ha traído un género de primera. ¿Desea que le recomiende nuestro famoso Arroz con Bogavante?"}
    ]

# Mostrar historial con burbujas personalizadas (SIN ROBOTS)
for message in st.session_state.messages:
    if message["role"] == "assistant":
        st.markdown(f'<div class="bot-bubble"><b>⚓ EL CAPITÁN:</b><br>{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="user-bubble">{message["content"]}</div>', unsafe_allow_html=True)

# Input del usuario
if prompt := st.chat_input("Hable con el Capitán..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# Respuesta simulada (Aquí iría tu lógica de LocalMind)
if st.session_state.messages[-1]["role"] == "user":
    with st.spinner(''):
        response = f"Excelente elección. El pescado que tenemos hoy se preparó a primera hora. Le sugiero acompañarlo con un **{data['menu']['bodega'][0]['nombre']}**. ¿Le parece bien?"
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# Branding
st.markdown("<br><center style='color: #888; font-size: 10px; letter-spacing: 2px;'>POWERED BY <b>LOCALMIND AI</b></center>", unsafe_allow_html=True)
