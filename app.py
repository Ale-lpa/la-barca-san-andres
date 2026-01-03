import streamlit as st
import google.generativeai as genai
import json

# ⚓ Configuración de página
st.set_page_config(page_title="La Barca de San Andrés", page_icon="⚓", layout="centered")

# --- CONEXIÓN CON GEMINI (IA) ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Configuramos el modelo con las instrucciones de personalidad desde el inicio
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction="Eres el Capitán de 'La Barca de San Andrés' (Gran Canaria, desde 1980). Tu tono es elegante y marinero. Responde en el idioma que te hablen. Sugiere siempre un vino de la carta (Yaiza Seco para pescado, Tirajanas para carnes/arroces). El pescado del día es Cherne o Abadejo (38€/kg). Sé breve y vendedor."
    )
except Exception as e:
    st.error("Error de configuración: Revisa la API KEY en Secrets.")
    st.stop()

# --- DISEÑO (Mantenemos tu estética impecable) ---
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
    .header-box { text-align: center; padding: 20px 10px 5px 10px; border-bottom: 2px solid #D4AF37; margin-bottom: 10px; }
    .header-box h1 { font-family: 'Playfair Display', serif; color: #D4AF37; font-size: 1.8rem; letter-spacing: 2px; margin: 0; text-transform: uppercase; }
    .header-box p { font-family: 'Poppins', sans-serif; color: #D4AF37; font-size: 0.7rem; letter-spacing: 3px; margin: 0; opacity: 0.9; }
    .chat-container { display: flex; flex-direction: column; gap: 15px; padding-bottom: 150px !important; }
    .bubble-assistant { background: rgba(0, 35, 102, 0.7); border-left: 5px solid #D4AF37; padding: 15px; border-radius: 5px 20px 20px 20px; color: #F9F7F2; font-family: 'Poppins', sans-serif; max-width: 85%; align-self: flex-start; }
    .bubble-user { background: rgba(212, 175, 55, 0.15); border-right: 5px solid #D4AF37; padding: 12px; border-radius: 20px 5px 20px 20px; color: #D4AF37; text-align: right; font-family: 'Poppins', sans-serif; max-width: 80%; align-self: flex-end; }
    .label-captain { color: #D4AF37; font-weight: 700; font-size: 0.7rem; margin-bottom: 5px; display: block; }
    div[data-testid="stChatInput"] { padding-bottom: 20px !important; }
    </style>
    <div class="header-box">
        <h1>⚓ LA BARCA DE SAN ANDRÉS ⚓</h1>
        <p>DESDE 1980</p>
    </div>
    """, unsafe_allow_html=True)

# --- CARGA DE LA CARTA ---
try:
    with open('knowledge.json', 'r', encoding='utf-8') as f:
        menu_context = f.read()
except:
    menu_context = "Carta no disponible."

# --- CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "model", "content": "¡Bienvenidos a bordo de La Barca de San Andrés! 🌊 Es un placer recibirles. Hoy el mar nos ha traído un género espectacular; ¿les gustaría probar nuestra recomendación del pescado del día?"}]

# Mostrar chat
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for m in st.session_state.messages:
    if m["role"] == "model":
        st.markdown(f'<div class="bubble-assistant"><span class="label-captain">⚓ EL CAPITÁN</span>{m["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bubble-user">{m["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Entrada de usuario
if prompt := st.chat_input("Hable con el Capitán..."):
    # Añadimos mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Preparamos el historial para Gemini (cambiando roles a los que él entiende)
    history = []
    for m in st.session_state.messages[:-1]:
        history.append({"role": m["role"], "parts": [m["content"]]})
    
    # Creamos la sesión de chat con la IA
    chat = model.start_chat(history=history)
    
    try:
        # Enviamos el contexto de la carta con la pregunta
        full_query = f"Contexto de la carta: {menu_context}\n\nPregunta del cliente: {prompt}"
        response = chat.send_message(full_query)
        st.session_state.messages.append({"role": "model", "content": response.text})
        st.rerun()
    except Exception as e:
        st.error(f"Error de conexión: {e}")

st.markdown("<center style='opacity:0.3; font-size:9px; color:white; margin-top:40px; letter-spacing:2px;'>LOCALMIND AI</center>", unsafe_allow_html=True)
