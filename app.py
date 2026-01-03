import streamlit as st
import google.generativeai as genai

# ⚓ Configuración de página
st.set_page_config(page_title="La Barca de San Andrés", page_icon="⚓", layout="centered")

# --- CONEXIÓN RESILIENTE (CON LIMPIEZA) ---
try:
    key = st.secrets["GOOGLE_API_KEY"].strip().replace('"', '').replace("'", "")
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Error de configuración de llave. Revisa los Secrets.")
    st.stop()

# --- DISEÑO ULTRA COMPACTO (Ajuste de espacios negros) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Poppins:wght@300;400;500&display=swap');
    
    /* Eliminar espacio superior de la app */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }

    .stApp {
        background: linear-gradient(rgba(0,0,0,0.96), rgba(0,0,0,0.96)), 
                    url('https://images.unsplash.com/photo-1550966841-391ad29a01d5?q=80&w=2070&auto=format&fit=crop'); 
        background-size: cover; background-attachment: fixed;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display:none;}

    /* 1. Ajuste espacio superior e inferior del nombre */
    .header-box { 
        text-align: center; 
        padding: 5px 10px 0px 10px; /* Casi sin espacio abajo */
        border-bottom: 2px solid #D4AF37; 
        margin-bottom: 10px; /* Pegamos el chat a la línea */
        margin-top: -30px; /* Subimos el logo al techo */
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
        padding-bottom: 5px;
        opacity: 0.9; 
    }

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
        max-width: 85%; 
        align-self: flex-start; 
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
        margin-bottom: 5px; 
        display: block; 
    }

    /* Barra de entrada */
    div[data-testid="stChatInput"] { padding-bottom: 20px !important; }
    </style>

    <div class="header-box">
        <h1>⚓ LA BARCA DE SAN ANDRÉS ⚓</h1>
        <p>DESDE 1980</p>
    </div>
    """, unsafe_allow_html=True)

# --- CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "model", "content": "¡Bienvenidos a bordo de La Barca de San Andrés! 🌊 Es un placer recibirles. ¿Les gustaría probar nuestra recomendación del pescado del día?"}]

st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for m in st.session_state.messages:
    if m["role"] == "model":
        st.markdown(f'<div class="bubble-assistant"><span class="label-captain">⚓ EL CAPITÁN</span>{m["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bubble-user">{m["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if prompt := st.chat_input("Hable con el Capitán..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Instrucciones simplificadas
    context = "Eres el Capitan de La Barca de San Andres. Habla en el idioma del cliente. Sugiere vino Yaiza o Tirajanas. Pescado del dia: Cherne (38e/kg)."
    
    try:
        response = model.generate_content(context + " Cliente: " + prompt)
        st.session_state.messages.append({"role": "model", "content": response.text})
        st.rerun()
    except:
        st.error("Error al generar respuesta. Revisa tu API KEY.")

st.markdown("<center style='opacity:0.2; font-size:9px; color:white; margin-top:20px;'>LOCALMIND AI</center>", unsafe_allow_html=True)
