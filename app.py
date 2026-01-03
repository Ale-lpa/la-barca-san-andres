import streamlit as st
import openai as genai

# ⚓ Configuración de página
st.set_page_config(page_title="La Barca de San Andrés", page_icon="⚓", layout="centered")

# --- CONEXIÓN IA CON LIMPIEZA DE LLAVE ---
try:
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("🚨 Falta la GOOGLE_API_KEY en los Secrets de Streamlit.")
        st.stop()
    
    key = st.secrets["GOOGLE_API_KEY"].strip().replace('"', '').replace("'", "")
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error de configuración de llave: {e}")
    st.stop()

# --- DISEÑO ULTRA COMPACTO (Adiós espacios negros) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Poppins:wght@300;400;500&display=swap');
    
    /* 1. Eliminar espacios muertos superiores e inferiores */
    .block-container {
        padding-top: 0.5rem !important;
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

    /* 2. Cabecera Pegada al Techo y Compacta */
    .header-box { 
        text-align: center; 
        padding: 0px 10px; 
        border-bottom: 2px solid #D4AF37; 
        margin-bottom: 15px; 
        margin-top: -45px; /* Sube el título al máximo */
    }
    
    .header-box h1 { 
        font-family: 'Playfair Display', serif; 
        color: #D4AF37; 
        font-size: 1.6rem; 
        letter-spacing: 2px; 
        margin: 0; 
        text-transform: uppercase; 
    }
    
    .header-box p { 
        font-family: 'Poppins', sans-serif; 
        color: #D4AF37; 
        font-size: 0.7rem; 
        letter-spacing: 3px; 
        margin: 0; 
        padding-bottom: 10px;
        opacity: 0.9; 
    }

    /* 3. Estética de las Burbujas */
    .chat-container { 
        display: flex; 
        flex-direction: column; 
        gap: 10px; 
        padding-bottom: 150px !important; 
    }

    .bubble-assistant { 
        background: rgba(0, 35, 102, 0.7); 
        border-left: 5px solid #D4AF37; 
        padding: 15px; 
        border-radius: 5px 20px 20px 20px; 
        color: #F9F7F2; 
        font-family: 'Poppins', sans-serif; 
        font-size: 0.95rem;
    }

    .bubble-user { 
        background: rgba(212, 175, 55, 0.15); 
        border-right: 5px solid #D4AF37; 
        padding: 12px; 
        border-radius: 20px 5px 20px 20px; 
        color: #D4AF37; 
        text-align: right; 
        font-family: 'Poppins', sans-serif; 
        font-size: 0.95rem;
        align-self: flex-end;
    }

    .label-captain { 
        color: #D4AF37; 
        font-weight: 700; 
        font-size: 0.7rem; 
        margin-bottom: 5px; 
        display: block; 
    }

    /* Barra de entrada de texto */
    div[data-testid="stChatInput"] { padding-bottom: 25px !important; }
    </style>

    <div class="header-box">
        <h1>⚓ LA BARCA DE SAN ANDRÉS ⚓</h1>
        <p>DESDE 1980</p>
    </div>
    """, unsafe_allow_html=True)

# --- SISTEMA DE CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "model", "content": "¡Bienvenidos a bordo de La Barca de San Andrés! 🌊 Es un placer recibirles. ¿Les gustaría probar nuestra recomendación del pescado del día?"}]

# Mostrar el historial
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for m in st.session_state.messages:
    if m["role"] == "model":
        st.markdown(f'<div class="bubble-assistant"><span class="label-captain">⚓ EL CAPITÁN</span>{m["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bubble-user">{m["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Entrada del usuario
if prompt := st.chat_input("Hable con el Capitán..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    contexto = "Eres el Capitán de La Barca de San Andrés. Habla en el idioma del cliente. Sugiere vino Yaiza o Tirajanas. Pescado: Cherne (38e/kg)."
    
    try:
        response = model.generate_content(contexto + " Cliente pregunta: " + prompt)
        st.session_state.messages.append({"role": "model", "content": response.text})
        st.rerun()
    except Exception as e:
        st.error(f"Error de conexión con la IA: {e}")

st.markdown("<center style='opacity:0.2; font-size:8px; color:white; margin-top:10px;'>LOCALMIND AI</center>", unsafe_allow_html=True)
