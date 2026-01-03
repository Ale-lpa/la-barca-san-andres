import streamlit as st
from openai import OpenAI

# ⚓ Configuración de página
st.set_page_config(page_title="La Barca de San Andrés", page_icon="⚓", layout="centered")

# --- CONEXIÓN CON OPENAI (Clave sk-...) ---
try:
    # Usamos el nombre 'OPENAI_API_KEY' para evitar confusiones
    if "OPENAI_API_KEY" in st.secrets:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"].strip())
    else:
        st.error("🚨 Falta la clave OPENAI_API_KEY en Secrets.")
        st.stop()
except Exception as e:
    st.error(f"Error de conexión: {e}")
    st.stop()

# --- DISEÑO (Espacio superior mantenido, espacio intermedio eliminado) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Poppins:wght@300;400;500&display=swap');
    
    /* Mantenemos el espacio superior como estaba */
    .block-container {
        padding-top: 4.5rem !important; 
        padding-bottom: 0rem !important;
        max-width: 500px;
    }
    
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.97), rgba(0,0,0,0.97)), 
                    url('https://images.unsplash.com/photo-1550966841-391ad29a01d5?q=80&w=2070&auto=format&fit=crop'); 
        background-size: cover; background-attachment: fixed;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display:none;}

    /* Ajuste de la cabecera */
    .header-box { 
        text-align: center; 
        padding: 10px 10px; 
        border-bottom: 2px solid #D4AF37; 
        margin-bottom: 5px; /* <-- CAMBIO AQUÍ: Reducido de 30px a 5px para pegar el chat */
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
        padding-bottom: 15px;
        opacity: 0.9; 
    }

    .chat-container { 
        display: flex; 
        flex-direction: column; 
        gap: 12px; 
        padding-bottom: 150px !important; 
    }

    .bubble-assistant { 
        background: rgba(0, 35, 102, 0.7); 
        border-left: 5px solid #D4AF37; 
        padding: 18px; 
        border-radius: 5px 20px 20px 20px; 
        color: #F9F7F2; 
        font-family: 'Poppins', sans-serif; 
    }

    .bubble-user { 
        background: rgba(212, 175, 55, 0.15); 
        border-right: 5px solid #D4AF37; 
        padding: 14px; 
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
        margin-bottom: 8px; 
        display: block; 
    }

    div[data-testid="stChatInput"] { padding-bottom: 30px !important; }
    
    .footer-brand {
        text-align: center;
        opacity: 0.3;
        font-size: 10px;
        color: white;
        letter-spacing: 4px;
        margin-top: 50px;
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
        {"role": "system", "content": "Eres el Capitán de La Barca de San Andrés. Habla siempre en el idioma que te hable el cliente. Sugiere siempre un vino (Yaiza o Tirajanas). Especialidad: Cherne o Abadejo (38€/kg). Tono elegante y servicial."},
        {"role": "assistant", "content": "¡Bienvenidos a bordo de La Barca de San Andrés! 🌊 Es un placer recibirles. ¿Les gustaría probar nuestra recomendación del pescado del día?"}
    ]

# Dibujar historial
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for m in st.session_state.messages:
    if m["role"] == "assistant":
        st.markdown(f'<div class="bubble-assistant"><span class="label-captain">⚓ EL CAPITÁN</span>{m["content"]}</div>', unsafe_allow_html=True)
    elif m["role"] == "user":
        st.markdown(f'<div class="bubble-user">{m["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Lógica de respuesta
if prompt := st.chat_input("Hable con el Capitán..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=st.session_state.messages
        )
        answer = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()
    except Exception as e:
        st.error(f"Error de OpenAI: {e}")

# Pie de página Localmind AI
st.markdown('<div class="footer-brand">LOCALMIND AI</div>', unsafe_allow_html=True)
