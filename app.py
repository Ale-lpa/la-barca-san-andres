import streamlit as st
import json

# Configuración de la página
st.set_page_config(page_title="La Barca de San Andrés", page_icon="⚓", layout="centered")

# --- DISEÑO RADICAL: ADIÓS STREAMLIT, HOLA LA BARCA ---
st.markdown("""
    <style>
    /* 1. Fondo de la Tarjeta (Madera/Bokeh) */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                    url('https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?auto=format&fit=crop&q=80&w=2070');
        background-size: cover;
        background-attachment: fixed;
    }

    /* 2. Cabecera Premium (Ancla y Pescado) */
    .header-barca {
        text-align: center;
        padding: 40px 0;
        border-bottom: 2px solid #C5A059;
        margin-bottom: 30px;
    }
    .nautical-logo { font-size: 60px; color: #C5A059; margin-bottom: 10px; }
    .header-barca h1 { font-family: 'Serif'; color: #C5A059; letter-spacing: 5px; text-transform: uppercase; font-size: 2.5rem; margin:0; }
    .header-barca p { color: white; letter-spacing: 8px; font-size: 0.7rem; opacity: 0.6; }

    /* 3. Burbujas de Chat Artesanales (Sin Robots) */
    .bubble-capitan {
        background: rgba(0, 35, 102, 0.7); /* Azul Marino */
        border-left: 5px solid #C5A059;
        padding: 20px;
        margin: 15px 0;
        border-radius: 5px 25px 25px 25px;
        color: #F9F7F2;
        max-width: 85%;
        box-shadow: 10px 10px 20px rgba(0,0,0,0.4);
    }
    .bubble-cliente {
        background: rgba(197, 160, 89, 0.2);
        border-right: 5px solid #C5A059;
        padding: 15px;
        margin: 15px 0;
        border-radius: 25px 5px 25px 25px;
        color: #C5A059;
        max-width: 80%;
        margin-left: auto;
        text-align: right;
    }

    /* 4. Ocultar elementos nativos de Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    .stChatInput { background-color: transparent !important; }
    .stChatInput div { border: 1px solid #C5A059 !important; border-radius: 50px !important; }
    </style>

    <div class="header-barca">
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
    st.error("Sube el archivo knowledge.json para que el Capitán sepa qué decir.")
    st.stop()

# Inicializar mensajes
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "¡Saludos! Soy el Capitán de La Barca. ⚓ Hoy el mar nos ha traído un género de primera. ¿Desea ver el pescado fresco o prefiere que le recomiende nuestro famoso Arroz con Bogavante?"}]

# Pintar el chat MANUALMENTE (Esto evita los robots)
for message in st.session_state.messages:
    if message["role"] == "assistant":
        st.markdown(f'<div class="bubble-capitan"><b>⚓ EL CAPITÁN:</b><br>{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bubble-cliente">{message["content"]}</div>', unsafe_allow_html=True)

# Input del usuario
if prompt := st.chat_input("Hable con el Capitán..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Aquí iría tu lógica de respuesta real. Para la demo:
    resp = f"Excelente elección. El pescado que tenemos hoy se preparó a primera hora. Le sugiero acompañarlo con un **{data['menu']['bodega'][0]['nombre']}**. ¿Le parece bien?"
    st.session_state.messages.append({"role": "assistant", "content": resp})
    st.rerun()
