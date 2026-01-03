import streamlit as st
import google.generativeai as genai
import json

# ⚓ Configuración de página
st.set_page_config(page_title="La Barca de San Andrés", page_icon="⚓", layout="centered")

# --- CONEXIÓN LIMPIA CON LA IA ---
try:
    # Limpieza profunda de la clave
    api_key_raw = st.secrets["GOOGLE_API_KEY"]
    api_key_clean = api_key_raw.strip().replace('"', '').replace("'", "")
    
    genai.configure(api_key=api_key_clean)
    
    # Usamos gemini-1.5-flash que es el más rápido para demos
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error de configuración: {e}")
    st.stop()

# --- DISEÑO (CSS PREMIUM) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Poppins:wght@300;400;500&display=swap');
    
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.95), rgba(0,0,0,0.95)), 
                    url('https://images.unsplash.com/photo-1550966841-391ad29a01d5?q=80&w=2070&auto=format&fit=crop'); 
        background-size: cover; background-attachment: fixed;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display:none;}

    .header-box {
        text-align: center;
        padding: 20px 10px 5px 10px; 
        border-bottom: 2px solid #D4AF37;
        margin-bottom: 20px; 
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
        margin: 0;
        text-transform: uppercase;
        opacity: 0.9;
    }

    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 15px;
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
        margin-bottom: 5px;
        display: block;
    }

    div[data-testid="stChatInput"] {
        padding-bottom: 20px !important;
    }
    </style>

    <div class="header-box">
        <h1>⚓ LA BARCA DE SAN ANDRÉS ⚓</h1>
        <p>DESDE 1980</p>
    </div>
    """, unsafe_allow_html=True)

# --- CARGA DE DATOS ---
try:
    with open('knowledge.json', 'r', encoding='utf-8') as f:
        carta = f.read()
except:
    carta = "Pescado fresco del día, Arroz con bogavante, Vinos canarios."

# --- CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "model", "content": "¡Bienvenidos a bordo de La Barca de San Andrés! 🌊 Es un placer recibirles. Hoy el mar nos ha traído un género espectacular; ¿les gustaría probar nuestra recomendación del pescado del día?"}]

# Renderizado de mensajes
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for m in st.session_state.messages:
    if m["role"] == "model":
        st.markdown(f'<div class="bubble-assistant"><span class="label-captain">⚓ EL CAPITÁN</span>{m["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bubble-user">{m["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Lógica de respuesta mejorada
if prompt := st.chat_input("Hable con el Capitán..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Prompt sin f-strings complejos para evitar errores de llaves
    instrucciones = "Eres el Capitán de La Barca de San Andrés. Habla en el idioma del cliente. Usa estos datos: " + carta + ". Sugiere siempre un vino (Yaiza o Tirajanas). Pescado del día: Cherne (38€/kg). Sé breve y elegante."
    pregunta_final = instrucciones + "\nCliente: " + prompt
    
    try:
        response = model.generate_content(pregunta_final)
        st.session_state.messages.append({"role": "model", "content": response.text})
        st.rerun()
    except Exception as e:
        st.error("Error al generar respuesta. Revisa tu API KEY.")

st.markdown("<center style='opacity:0.2; font-size:9px; color:white; margin-top:40px;'>LOCALMIND AI</center>", unsafe_allow_html=True)
