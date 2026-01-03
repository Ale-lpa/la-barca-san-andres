import streamlit as st
import json

# Configuración de página
st.set_page_config(page_title="La Barca - Capitán Virtual", page_icon="⚓", layout="centered")

# --- EL CAMBIO ESTÉTICO TOTAL (CSS) ---
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

    /* 2. LOGO PERSONALIZADO (Ancla y Pescado) */
    .header-box {
        text-align: center;
        padding: 40px 10px;
        border-bottom: 2px solid #D4AF37;
        margin-bottom: 40px;
    }
    .nautical-icon {
        font-size: 60px;
        color: #D4AF37; /* Dorado */
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

    /* 3. BORRAR EL ROBOT Y LOS AVATARES (Cirugía Estética) */
    [data-testid="stChatMessageAvatarAssistant"], 
    [data-testid="stChatMessageAvatarUser"],
    .st-emotion-cache-12w0qpk { /* Ocultar el círculo del avatar */
        display: none !important;
    }

    /* 4. BURBUJAS DE CHAT PERSONALIZADAS */
    .chat-bubble-assistant {
        background: rgba(0, 35, 102, 0.6); /* Azul marino elegante */
        border-left: 4px solid #D4AF37;
        padding: 20px;
        border-radius: 4px 20px 20px 20px;
        margin-bottom: 25px;
        color: #F9F7F2;
        font-family: 'Poppins', sans-serif;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.3);
        max-width: 90%;
    }

    .chat-bubble-user {
        background: rgba(212, 175, 55, 0.1);
        border-right: 4px solid #D4AF37;
        padding: 15px;
        border-radius: 20px 4px 20px 20px;
        margin-bottom: 25px;
        color: #D4AF37;
        text-align: right;
        font-family: 'Poppins', sans-serif;
        margin-left: auto;
        max-width: 80%;
    }

    /* 5. INPUT DE TEXTO (Minimalista) */
    .stChatInput {
        background-color: transparent !important;
    }
    .stChatInput > div {
        border: 1px solid #D4AF37 !important;
        border-radius: 5px !important;
        background: rgba(255,255,255,0.05) !important;
    }
    .stChatInput textarea {
        color: white !important;
    }

    /* Ocultar bordes de Streamlit */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        padding: 0 !important;
    }
    </style>

    <div class="header-box">
        <div class="nautical-icon">⚓🐟</div>
        <h1>
