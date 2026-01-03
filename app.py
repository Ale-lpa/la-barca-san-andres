import streamlit as st
import json

# Configuración de página
st.set_page_config(page_title="La Barca de San Andrés", page_icon="⚓", layout="centered")

# --- DISEÑO REFINADO: FONDO MÁS OSCURO Y AJUSTE DE POSICIÓN ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Poppins:wght@300;400;500&display=swap');

    /* 1. Fondo con negro más profundo (0.95 de opacidad) */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.95), rgba(0,0,0,0.95)), 
                    url('https://images.unsplash.com/photo-1550966841-391ad29a01d5?q=80&w=2070&auto=format&fit=crop'); 
        background-size: cover;
        background-attachment: fixed;
    }

    /* Ocultamos elementos estándar de Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display:none;}

    /* 2. Ajuste del Header para que el chat suba */
    .header-box {
        text-align: center;
        padding: 20px 10px 10px 10px; /* Reducimos el relleno */
        border-bottom: 2px solid #D4AF37;
        margin-bottom: 15px; /* Reducimos el margen para subir el mensaje */
    }
    .nautical-icon {
        font-size: 50px;
        color: #D4AF37;
        margin-bottom: 0px;
    }
    .header-box h1 {
        font-family: 'Playfair Display', serif;
        color: #D4AF37;
        font-size: 2rem; 
        letter-spacing: 4px;
        margin: 0;
        text-transform: uppercase;
    }

    /* 3. Contenedor de Chat y Burbujas */
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 15px;
        padding: 10px;
        padding-bottom: 120px !important; 
    }

    .bubble-assistant {
        background: rgba(0, 35, 102, 0.7); 
        border-left: 5px solid #D4AF37;
        padding: 15px;
        border-radius: 5px 20px 20px 20px;
        color: #F9F7F2;
        font-family: 'Poppins', sans-serif;
        max-width: 85%;
        align-self: flex-start;
        box-shadow: 8px 8px 20px rgba(0,0,0,0.4);
    }

    .bubble-user {
        background: rgba(212, 175, 55, 0.15);
        border-right: 5px solid #D4AF37;
        padding: 12px;
        border-radius: 20px 5px 20px 20px;
        color: #D4AF37;
        text-align: right;
        font-family: 'Poppins', sans-serif;
        max-width: 80%;
        align-self: flex-end;
    }

    .label-captain {
        color: #D4AF37;
        font-weight: 700;
        font-size: 0.7rem;
        letter-spacing: 2px;
        margin-bottom: 5px;
        display: block;
    }

    /* Estilo de la barra de entrada */
    div[data-testid="stChatInput"] {
        padding-bottom: 20px !important;
        background-color: transparent !important;
    }
    </style>

    <div class="header-box">
        <div class="nautical-icon">⚓🐟</div>
        <h1>LA BARCA DE SAN ANDRÉS</h1>
    </div>
    """, unsafe_allow_html=True)

# --- CARGA DE DATOS ---
try:
    with open('knowledge.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except:
    st.error("Archivo knowledge.json no encontrado.")
    st.stop()

# --- HISTORIAL DE CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Bienvenido a bordo! Soy el Capitán de La Barca. ⚓ ¿En qué idioma desea que le ayude hoy?"}
    ]

# Dibujamos los mensajes
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

# --- ENTRADA DE USUARIO ---
if prompt := st.chat_input("Hable con el Capitán..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Respuesta basada en el JSON
    response = f"Excelente elección. Nuestro pescado fresco hoy está de categoría. Le sugiero acompañarlo con un vino de nuestra bodega. ¿Le parece bien?"
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

st.markdown("<center style='opacity:0.3; font-size:9px; color:white; margin-top:40px; letter-spacing:2px;'>LOCALMIND AI</center>", unsafe_allow_html=True)
