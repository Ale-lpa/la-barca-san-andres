import streamlit as st
from openai import OpenAI

# ⚓ Configuración de página
st.set_page_config(page_title="La Barca de San Andrés", page_icon="⚓", layout="centered")

# --- CONEXIÓN CON OPENAI ---
try:
    api_key = st.secrets["OPENAI_API_KEY"].strip()
    client = OpenAI(api_key=api_key)
except Exception as e:
    st.error("Revisa la clave OPENAI_API_KEY en los Secrets.")
    st.stop()

# --- DISEÑO AJUSTADO: ESPACIOS MÍNIMOS Y ESTÉTICOS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Poppins:wght@300;400;500&display=swap');
    
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.96), rgba(0,0,0,0.96)), 
                    url('https://images.unsplash.com/photo-1550966841-391ad29a01d5?q=80&w=2070&auto=format&fit=crop'); 
        background-size: cover; background-attachment: fixed;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display:none;}

    /* Contenedor del Título: Ultra compacto y centrado */
    .header-box {
        text-align: center;
        padding-top: 10px;    /* Espacio mínimo al techo */
        padding-bottom: 5px;  /* Espacio mínimo a la línea */
        border-bottom: 1px solid #D4AF37;
        margin-bottom: 15px;  /* Separación estética al chat */
    }
    
    .header-box h1 {
        font-family: 'Playfair Display', serif;
        color: #D4AF37;
        font-size: 1.7rem; 
        letter-spacing: 3px;
        margin: 0;
        text-transform: uppercase;
    }

    .header-box p {
        font-family: 'Poppins', sans-serif;
        color: #D4AF37;
        font-size: 0.65rem;
        letter-spacing: 4px;
        margin: 2px 0 0 0;
        opacity: 0.8;
    }

    /* Contenedor de Chat: Subimos los mensajes */
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 12px;
        padding-top: 0px; 
        padding-bottom: 140px !important; 
    }

    .bubble-assistant {
        background: rgba(0, 35, 102, 0.7); 
        border-left: 4px solid #D4AF37;
        padding: 14px;
        border-radius: 5px 18px 18px 18px;
        color: #F9F7F2;
        font-family: 'Poppins', sans-serif;
        max-width: 88%;
        align-self: flex-start;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.3);
        font-size: 0.95rem;
    }

    .bubble-user {
        background: rgba(212, 175, 55, 0.12);
        border-right: 4px solid #D4AF37;
        padding: 10px;
        border-radius: 18px 5px 18px 18px;
        color: #D4AF37;
        text-align: right;
        font-family: 'Poppins', sans-serif;
        max-width: 80%;
        align-self: flex-end;
        font-size: 0.9rem;
    }

    .label-captain {
        color: #D4AF37;
        font-weight: 700;
        font-size: 0.65rem;
        letter-spacing: 1.5px;
        margin-bottom: 4px;
        display: block;
    }

    /* Estilo del Input */
    div[data-testid="stChatInput"] {
        padding-bottom: 25px !important;
    }
    </style>

    <div class="header-box">
        <h1>⚓ LA BARCA DE SAN ANDRÉS ⚓</h1>
        <p>DESDE 1980</p>
    </div>
    """, unsafe_allow_html=True)

# --- CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Eres el Capitán de La Barca de San Andrés. Responde en el idioma del cliente. Sugiere vino Yaiza o Tirajanas. Pescado: Cherne a 38€/kg. Tono elegante."},
        {"role": "assistant", "content": "¡Bienvenidos a bordo de La Barca de San Andrés! 🌊 Es un placer recibirles. ¿Les gustaría probar nuestra recomendación del pescado del día?"}
    ]

# Renderizado de mensajes sin espacios muertos arriba
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for m in st.session_state.messages:
    if m["role"] == "assistant":
        st.markdown(f'<div class="bubble-assistant"><span class="label-captain">⚓ EL CAPITÁN</span>{m["content"]}</div>', unsafe_allow_html=True)
    elif m["role"] == "user":
        st.markdown(f'<div class="bubble-user">{m["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Lógica
if prompt := st.chat_input("Escriba aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages
        )
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.rerun()
    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("<center style='opacity:0.2; font-size:9px; color:white; margin-top:20px;'>LOCALMIND AI</center>", unsafe_allow_html=True)
