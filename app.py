import streamlit as st
import google.generativeai as genai
import json

# ⚓ Configuración de página
st.set_page_config(page_title="La Barca de San Andrés", page_icon="⚓", layout="centered")

# --- CONEXIÓN CON EL CEREBRO (GEMINI) ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("⚠️ Configura la GOOGLE_API_KEY en los Secrets de Streamlit.")
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

# --- CARGA DE DATOS DE LA CARTA ---
with open('knowledge.json', 'r', encoding='utf-8') as f:
    menu_context = f.read()

# --- PROMPT DEL CAPITÁN (Instrucciones de personalidad) ---
SYSTEM_PROMPT = f"""
Eres el Capitán de 'La Barca de San Andrés', un restaurante emblemático fundado en 1980 en Gran Canaria.
Tu personalidad: Elegante, experto, marinero de vieja escuela y gran anfitrión.
Tu misión:
1. Habla en CUALQUIER idioma que el cliente use (más de 50 idiomas).
2. Usa SIEMPRE los datos reales de la carta que te doy aquí: {menu_context}.
3. VENTA SUGERIDA: Por cada plato o entrante que el cliente mencione, sugiere SIEMPRE un vino de nuestra bodega que maride bien (especialmente el Yaiza Seco para pescados o Tirajanas para carnes/arroces).
4. Si preguntan por el pescado del día, menciona el Cherne o Abadejo a 38€/kg y sugiere acompañarlo con un vino blanco frío.
5. Sé breve, elegante y termina siempre con una invitación a pedir o reservar.
"""

# --- FLUJO DEL CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "¡Bienvenidos a bordo de La Barca de San Andrés! 🌊 Es un placer recibirles. Hoy el mar nos ha traído un género espectacular; ¿les gustaría probar nuestra recomendación del pescado del día?"}]

st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for m in st.session_state.messages:
    cls = "bubble-assistant" if m["role"] == "assistant" else "bubble-user"
    lbl = '<span class="label-captain">⚓ EL CAPITÁN</span>' if m["role"] == "assistant" else ""
    st.markdown(f'<div class="{cls}">{lbl}{m["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if prompt := st.chat_input("Hable con el Capitán..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Llamada a Gemini con todo el contexto
    full_prompt = f"{SYSTEM_PROMPT}\n\nHistorial de chat:\n"
    for m in st.session_state.messages:
        full_prompt += f"{m['role']}: {m['content']}\n"
    
    response = model.generate_content(full_prompt)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
    st.rerun()

