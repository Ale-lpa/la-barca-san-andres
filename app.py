import streamlit as st
import json

# Configuración de página
st.set_page_config(page_title="La Barca de San Andrés - Capitán Virtual", page_icon="⚓", layout="centered")

# --- DISEÑO FINAL: ESTILO TABERNA Y ESPACIO INFERIOR ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Poppins:wght@300;400;500&display=swap');

    /* 1. Fondo y Espacio Inferior (para evitar que se corte el input) */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
                    url('https://images.unsplash.com/photo-1550966841-391ad29a01d5?q=80&w=2070&auto=format&fit=crop'); 
        background-size: cover;
        background-attachment: fixed;
        padding-bottom: 100px !important; /* Espacio extra al final */
    }

    /* Ocultamos elementos estándar de Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display:none;}

    /* 2. Logo con el nombre corregido */
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
    }
    .header-box h1 {
        font-family: 'Playfair Display', serif;
        color: #D4AF37;
        font-size: 2.8rem;
        letter-spacing: 5px;
        margin: 0;
        text-transform: uppercase;
    }
    .header-box p {
        font-family: 'Poppins', sans-serif;
        color: white;
        letter-spacing: 8px;
        font-size: 0.8rem;
        text-transform: uppercase;
        opacity: 0.6;
    }

    /* 3. Burbujas de Chat Personalizadas (Sin el robot) */
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
    }

    .label-captain {
        color: #D4AF37;
        font-weight: 700;
        font-size: 0.7rem;
        letter-spacing: 2px;
        margin-bottom: 8px;
        display: block;
    }

    /* Ajuste para que el input flote correctamente */
    .stChatInput {
        background-color: rgba(0,0,0,0.5) !important;
        padding-bottom: 20px !important;
    }
    </style>

    <div class="header-box
