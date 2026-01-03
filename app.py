import streamlit as st
import json

# ⚓ Configuración de página
st.set_page_config(page_title="La Barca de San Andrés", page_icon="⚓", layout="centered")

# --- DISEÑO COMPACTO: ANCLAS LATERALES Y ESPACIO MÍNIMO ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Poppins:wght@300;400;500&display=swap');

    /* 1. Fondo con negro profundo */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.95), rgba(0,0,0,0.95)), 
                    url('https://images.unsplash.com/photo-1550966841-391ad29a01d5?q=80&w=2070&auto=format&fit=crop'); 
        background-size: cover;
        background-attachment: fixed;
    }

    /* Ocultamos elementos estándar de Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display:none;}

    /* 2. Cabecera ultra compacta */
    .header-box {
        text-align: center;
        padding: 10px 10px 2px 10px; /* Espacio mínimo arriba y abajo */
        border-bottom: 2px solid #D4AF37;
        margin-bottom: 5px; /* Sube el chat casi pegado a la línea */
    }
    
    .header-box h1 {
        font-family: 'Playfair Display', serif;
        color: #D4AF37;
        font-size: 1.8rem; 
        letter-spacing: 2px;
        margin: 0;
        text-transform: uppercase;
    }

    .header-box p {
        font-family: 'Poppins', sans-serif;
        color: #D4AF37;
        font-size: 0.7rem;
        letter-spacing: 3px;
        margin-top: 0px;
        margin-bottom: 5px;
        text-transform: uppercase;
        opacity: 0.9;
    }

    /* 3. Contenedor de Chat */
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 15px;
        padding: 5px 10px;
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
        font-size:
