import streamlit as st
from openai import OpenAI

# ⚓ Configuración de página
st.set_page_config(page_title="La Barca de San Andrés", page_icon="⚓", layout="centered")

# --- CONEXIÓN CON OPENAI (Clave sk-...) ---
try:
    if "OPENAI_API_KEY" in st.secrets:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"].strip())
    else:
        st.error("🚨 Falta la clave OPENAI_API_KEY en Secrets.")
        st.stop()
except Exception as e:
    st.error(f"Error de conexión: {e}")
    st.stop()

# --- DISEÑO ULTRA COMPACTO (Ajuste final de espacios) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Poppins:wght@300;400;500&display=swap');
    
    /* 1. Reducir el espacio superior (Techo) */
    .block-container {
        padding-top: 1.5rem !important; /* Bajado de 4.5rem a 1.5rem */
        padding-bottom: 0rem !important;
        max-width: 500px;
    }
    
    /* Eliminar el header vacío de Streamlit que ocupa espacio negro */
    header {visibility: hidden !important; height: 0px !important;}

    .stApp {
        background: linear-gradient(rgba(0,0,0,0.97), rgba(0,0,0,0.97)), 
                    url('https://images.unsplash.com/photo-1550966841-391ad29a01d5?q=80&w=2070&auto=format&fit=crop'); 
        background-size: cover; background-attachment: fixed;
    }
    
    #MainMenu, footer {visibility: hidden;}
    .stDeployButton {display:none;}

    /* 2. Ajuste de la cabecera (Zona Intermedia) */
    .header-box { 
        text-align: center; 
        padding: 0px 10px; 
        border-bottom: 2px solid #D4AF37; 
        margin-bottom: -45px !important; /* Margen negativo agresivo para pegar el chat */
        z-index: 100;
        position: relative;
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
        font-size: 0.75rem; 
        letter-spacing: 3px; 
        margin: 0; 
        padding-bottom: 8px;
        opacity: 0.9; 
    }

    /* 3. Contenedor del chat */
    .chat-container { 
        display: flex; 
        flex-direction: column; 
        gap: 10px; 
        padding-top: 0px !important;
        padding-bottom: 140px !important; 
    }

    .bubble-assistant { 
        background: rgba(0, 35, 102, 0.7); 
        border-left: 5px solid #D4AF37; 
        padding: 16px; 
        border-radius: 5px 20px 20px 20px; 
        color: #F9F7F2; 
        font-family: 'Poppins', sans-serif; 
    }

    .bubble-user { 
        background: rgba(212, 175, 55, 0.15); 
        border-right: 5px solid #D4AF37; 
        padding: 12px; 
        border-radius: 20px 5px 20px 20px; 
        color: #D4AF37; 
        text-align: right; 
        font-family: 'Poppins', sans-serif; 
        align-self: flex-end;
    }

    .label-captain { 
        color: #D4AF37; 
        font-weight: 700; 
        font-size: 0.75rem; 
        margin-bottom: 6px; 
        display: block; 
    }

    div[data-testid="stChatInput"] { padding-bottom: 25px !important; }
    
    /* Footer Localmind AI */
    .footer-brand {
        text-align: center;
        opacity: 0.3;
        font-size: 9px;
        color: white;
        letter-spacing: 4px;
        margin-top: 20px;
        padding-bottom: 20px;
        font-family: 'Poppins', sans-serif;
        text-transform: uppercase;
    }
    </style>

    <div class="header-box">
        <h1>⚓ LA BARCA DE SAN ANDRÉS ⚓</h1>
        <p>DESDE 1980</p>
    </div>
    """, unsafe_allow_html=True)

# --- SISTEMA DE CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Eres el Capitán de La Barca de San Andrés. Habla siempre en el idioma del cliente. Sugiere siempre un vino (Yaiza o Tirajanas). Especialidad: Cherne o Abadejo (38€/kg). Tono elegante y servicial."},
        {"role": "assistant", "content": "¡Bienvenidos a bordo de La Barca de San Andrés! 🌊 Es un placer recibirles. ¿Les gustaría probar nuestra recomendación del pescado del día?"}
    ]

# Renderizado pegado a la línea
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for m in st.session_state.messages:
    if m["role"] == "assistant":
        st.markdown(f'<div class="bubble-assistant"><span class="label-captain">⚓ EL CAPITÁN</span>{m["content"]}</div>', unsafe_allow_html=True)
    elif m["role"] == "user":
        st.markdown(f'<div class="bubble-user">{m["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if prompt := st.chat_input("Hable con el Capitán..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        )
        answer = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()
    except Exception as e:
        st.error(f"Error: {e}")

st.markdown('<div class="footer-brand">LOCALMIND AI</div>', unsafe_allow_html=True)
