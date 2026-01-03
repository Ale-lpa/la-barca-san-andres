import streamlit as st
import google.generativeai as genai
import json

# ⚓ Configuración de página
st.set_page_config(page_title="La Barca de San Andrés", page_icon="⚓", layout="centered")

# --- CONEXIÓN DE EMERGENCIA CON IA ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"].strip()
    genai.configure(api_key=api_key)
    
    # Intentamos el modelo Flash, y si da error 404, usamos el Pro automáticamente
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        # Prueba rápida de conexión
        model.generate_content("hola") 
    except:
        model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error("Error de configuración de la llave API.")
    st.stop()

# --- DISEÑO (Tu estética premium) ---
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
    .header-box h1 { font-family: 'Playfair Display', serif; color: #D4AF37; font-size: 1.8rem; letter-spacing: 4px; margin: 0; text-transform: uppercase; }
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

# --- DATOS DE LA CARTA ---
try:
    with open('knowledge.json', 'r', encoding='utf-8') as f:
        menu_info = f.read()
except:
    menu_info = "Pescado del día: Cherne. Especialidad: Arroz con Bogavante. Vinos: Yaiza, Tirajanas."

# --- CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "model", "content": "¡Bienvenidos a bordo de La Barca de San Andrés! 🌊 Es un placer recibirles. ¿Les gustaría probar nuestra recomendación del pescado del día?"}]

# Renderizado
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for m in st.session_state.messages:
    if m["role"] == "model":
        st.markdown(f'<div class="bubble-assistant"><span class="label-captain">⚓ EL CAPITÁN</span>{m["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bubble-user">{m["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Lógica de respuesta
if prompt := st.chat_input("Escriba al Capitán..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Contexto para que hable 50 idiomas y venda vino
    instrucciones = f"""
    Eres el Capitán de La Barca de San Andrés. 
    1. Responde en el idioma del cliente ({prompt}).
    2. Usa estos datos: {menu_info}.
    3. Sugiere SIEMPRE maridar con vino (Yaiza Seco o Tirajanas).
    4. Tono: Elegante y marinero.
    """
    
    try:
        response = model.generate_content(f"{instrucciones}\n\nCliente dice: {prompt}")
        st.session_state.messages.append({"role": "model", "content": response.text})
        st.rerun()
    except Exception as e:
        st.error(f"Error de conexión: {e}")
