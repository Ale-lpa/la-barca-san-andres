import streamlit as st
import json

# Configuración de página
st.set_page_config(page_title="La Barca - Capitán Virtual", page_icon="⚓", layout="centered")

# --- CSS RADICAL (Ignoramos los componentes de Streamlit) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Poppins:wght@300;400;500&display=swap');

    /* 1. FONDO DE TABERNA PREMIUM (Cálido y Oscuro) */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
                    url('https://images.unsplash.com/photo-1550966841-391ad29a01d5?q=80&w=2070&auto=format&fit=crop'); 
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Ocultamos los elementos nativos de Streamlit que sobran */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display:none;}

    /* 2. LOGO PERSONALIZADO (Ancla y Pescado) */
    .header-box {
        text-align: center;
        padding: 40px 10px;
        border-bottom: 2px solid #D4AF37;
        margin-bottom: 40px;
    }
    .nautical-icon {
        font-size: 60px;
        color: #D4AF37;
        margin-bottom: 5px;
        filter: drop-shadow(0px 0px 10px rgba(212, 175, 55, 0.4));
    }
    .header-box h1 {
        font-family: 'Playfair Display', serif;
        color: #D4AF37;
        font-size: 3rem;
        letter-spacing: 8px;
        margin: 0;
        text-transform: uppercase;
    }
    .header-box p {
        font-family: 'Poppins', sans-serif;
        color: white;
        letter-spacing: 10px;
        font-size: 0.7rem;
        text-transform: uppercase;
        opacity: 0.6;
    }

    /* 3. BURBUJAS DE CHAT 100% PERSONALIZADAS (HTML PURO) */
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 20px;
        padding: 10px;
    }

    .bubble-assistant {
        background: rgba(0, 35, 102, 0.7); /* Azul marino */
        border-left: 5px solid #D4AF37;
        padding: 20px;
        border-radius: 5px 25px 25px 25px;
        color: #F9F7F2;
        font-family: 'Poppins', sans-serif;
        max-width: 85%;
        align-self: flex-start;
        box-shadow: 8px 8px 20px rgba(0,0,0,0.4);
    }

    .bubble-user {
        background: rgba(212, 175, 55, 0.15);
        border-right: 5px solid #D4AF37;
        padding: 15px;
        border-radius: 25px 5px 25px 25px;
        color: #D4AF37;
        text-align: right;
        font-family: 'Poppins', sans-serif;
        max-width: 80%;
        align-self: flex-end;
        box-shadow: -5px 5px 15px rgba(0,0,0,0.2);
    }

    .label-captain {
        color: #D4AF37;
        font-weight: 700;
        font-size: 0.7rem;
        letter-spacing: 2px;
        margin-bottom: 8px;
        display: block;
    }

    /* 4. EL INPUT DE TEXTO */
    .stChatInput {
        border-top: 1px solid rgba(212,175,55,0.3) !important;
        padding-top: 20px !important;
    }
    </style>

    <div class="header-box">
        <div class="nautical-icon">⚓🐟</div>
        <h1>LA BARCA</h1>
        <p>SAN ANDRÉS</p>
    </div>
    """, unsafe_allow_html=True)

# --- CARGA DE DATOS ---
try:
    with open('knowledge.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except:
    st.error("Archivo knowledge.json no encontrado.")
    st.stop()

# --- LÓGICA DE CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Bienvenido a bordo! Soy el Capitán de La Barca. ⚓ Hoy el mar nos ha traído un género espectacular. ¿Desea ver el pescado fresco o prefiere que le recomiende nuestra especialidad?"}
    ]

# Dibujamos el chat usando HTML (esto ignora los robots de Streamlit)
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for message in st.session_state.messages:
    if message["role"] == "assistant":
        st.markdown(f'''
            <div class="bubble-assistant">
                <span class="label-captain">⚓ EL CAPITÁN</span>
                {message["content"]}
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
            <div class="bubble-user">
                {message["content"]}
            </div>
        ''', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Input
if prompt := st.chat_input
