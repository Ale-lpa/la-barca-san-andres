import streamlit as st
from openai import OpenAI

# ⚓ Configuración de página
st.set_page_config(page_title="La Barca de San Andrés", page_icon="⚓", layout="centered")

# --- OPTIMIZACIÓN 1: Caché de Conexión ---
@st.cache_resource
def get_openai_client():
    return OpenAI(api_key=st.secrets["OPENAI_API_KEY"].strip())

try:
    client = get_openai_client()
except Exception as e:
    st.error("Error de conexión.")
    st.stop()

# --- DISEÑO (Optimizado para carga rápida) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Poppins:wght@300;400;500&display=swap');
    
    .block-container { padding-top: 1.5rem !important; padding-bottom: 1rem !important; max-width: 500px; }
    header {visibility: hidden !important; height: 0px !important;}
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.97), rgba(0,0,0,0.97)), 
                    url('https://images.unsplash.com/photo-1550966841-391ad29a01d5?q=20&w=800&auto=format&fit=crop'); 
        background-size: cover; background-attachment: fixed;
    }
    #MainMenu, footer, .stDeployButton {display:none !important;}

    .header-box { 
        text-align: center; border-bottom: 2px solid #D4AF37; 
        margin-bottom: -45px !important; z-index: 100; position: relative;
    }
    .header-box h1 { font-family: 'Playfair Display', serif; color: #D4AF37; font-size: 1.8rem; margin: 0; text-transform: uppercase; }
    .header-box p { font-family: 'Poppins', sans-serif; color: #D4AF37; font-size: 0.75rem; letter-spacing: 3px; margin: 0; padding-bottom: 8px; opacity: 0.9; }

    .chat-container { display: flex; flex-direction: column; gap: 10px; padding-bottom: 80px !important; }
    .bubble-assistant { background: rgba(0, 35, 102, 0.7); border-left: 5px solid #D4AF37; padding: 16px; border-radius: 5px 20px 20px 20px; color: #F9F7F2; font-family: 'Poppins', sans-serif; }
    .bubble-user { background: rgba(212, 175, 55, 0.15); border-right: 5px solid #D4AF37; padding: 12px; border-radius: 20px 5px 20px 20px; color: #D4AF37; text-align: right; font-family: 'Poppins', sans-serif; align-self: flex-end; }
    .label-captain { color: #D4AF37; font-weight: 700; font-size: 0.75rem; margin-bottom: 6px; display: block; }

    div[data-testid="stChatInput"] { padding-bottom: 10px !important; }
    .footer-brand { text-align: center; opacity: 0.3; font-size: 9px; color: white; letter-spacing: 4px; margin-top: 5px; padding-bottom: 5px; font-family: 'Poppins', sans-serif; text-transform: uppercase; }
    </style>

    <div class="header-box">
        <h1>⚓ LA BARCA DE SAN ANDRÉS ⚓</h1>
        <p>DESDE 1980</p>
    </div>
    """, unsafe_allow_html=True)

# --- SISTEMA DE CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Eres el Capitán de La Barca de San Andrés. Explica platos y sugiere vinos (Yaiza o Tirajanas). Cherne/Abadejo (38€/kg). Sé breve, elegante y experto."},
        {"role": "assistant", "content": "¡Bienvenidos a bordo! 🌊 Hoy el mar nos ha traído un género espectacular; ¿les gustaría probar nuestra recomendación del día?"}
    ]

# Renderizado de historial
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for m in st.session_state.messages:
    if m["role"] == "assistant":
        st.markdown(f'<div class="bubble-assistant"><span class="label-captain">⚓ EL CAPITÁN</span>{m["content"]}</div>', unsafe_allow_html=True)
    elif m["role"] == "user":
        st.markdown(f'<div class="bubble-user">{m["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- OPTIMIZACIÓN 2: Lógica de Streaming ---
if prompt := st.chat_input("Hable con el Capitán..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Mostrar el mensaje del usuario inmediatamente
    st.markdown(f'<div class="bubble-user">{prompt}</div>', unsafe_allow_html=True)
    
    # Crear el contenedor para la respuesta del Capitán
    with st.chat_message("assistant", avatar=None):
        # Ocultamos el diseño por defecto de Streamlit y usamos nuestra burbuja
        st.markdown('<div class="bubble-assistant"><span class="label-captain">⚓ EL CAPITÁN</span>', unsafe_allow_html=True)
        
        response_placeholder = st.empty()
        full_response = ""
        
        # Llamada con Streaming
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                response_placeholder.markdown(full_response + "▌")
        
        response_placeholder.markdown(full_response)
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.rerun()

st.markdown('<div class="footer-brand">LOCALMIND AI</div>', unsafe_allow_html=True)
