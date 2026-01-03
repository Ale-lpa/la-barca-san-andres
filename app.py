import streamlit as st
import google.generativeai as genai

# ⚓ Configuración de página
st.set_page_config(page_title="La Barca de San Andrés", page_icon="⚓", layout="centered")

# --- AUTO-DIAGNÓSTICO DE LLAVE ---
try:
    # 1. Limpieza absoluta de la clave
    raw_key = st.secrets["GOOGLE_API_KEY"]
    clean_key = raw_key.strip().replace('"', '').replace("'", "").replace(" ", "")
    
    # 2. Configuración
    genai.configure(api_key=clean_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # 3. Verificación visual para ti (puedes borrar esto después)
    # Mostramos los primeros 4 y últimos 4 caracteres para confirmar que es la correcta
    st.sidebar.success(f"Sistema listo. Clave detectada: {clean_key[:4]}...{clean_key[-4:]}")

except Exception as e:
    st.error(f"🚨 ERROR CRÍTICO: El sistema no encuentra la llave. {e}")
    st.info("Asegúrate de que en Secrets pusiste: GOOGLE_API_KEY = 'tu_clave'")
    st.stop()

# --- DISEÑO PREMIUM ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Poppins:wght@300;400;500&display=swap');
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.95), rgba(0,0,0,0.95)), 
                    url('https://images.unsplash.com/photo-1550966841-391ad29a01d5?q=80&w=2070&auto=format&fit=crop'); 
        background-size: cover; background-attachment: fixed;
    }
    #MainMenu, footer, header {visibility: hidden;}
    .header-box { text-align: center; padding: 20px 10px 5px 10px; border-bottom: 2px solid #D4AF37; margin-bottom: 20px; }
    .header-box h1 { font-family: 'Playfair Display', serif; color: #D4AF37; font-size: 1.8rem; letter-spacing: 4px; margin: 0; text-transform: uppercase; }
    .header-box p { font-family: 'Poppins', sans-serif; color: #D4AF37; font-size: 0.7rem; letter-spacing: 3px; margin: 0; opacity: 0.9; }
    .chat-container { display: flex; flex-direction: column; gap: 15px; padding-bottom: 150px !important; }
    .bubble-assistant { background: rgba(0, 35, 102, 0.7); border-left: 5px solid #D4AF37; padding: 15px; border-radius: 5px 20px 20px 20px; color: #F9F7F2; font-family: 'Poppins', sans-serif; max-width: 85%; align-self: flex-start; }
    .bubble-user { background: rgba(212, 175, 55, 0.15); border-right: 5px solid #D4AF37; padding: 12px; border-radius: 20px 5px 20px 20px; color: #D4AF37; text-align: right; font-family: 'Poppins', sans-serif; max-width: 80%; align-self: flex-end; }
    div[data-testid="stChatInput"] { padding-bottom: 20px !important; }
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
    carta = "Pescado del día: Cherne (38€/kg). Vinos: Yaiza Seco."

# --- CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "model", "content": "¡Bienvenidos a bordo! 🌊 Soy el Capitán. ¿Desean probar nuestra recomendación del pescado del día?"}]

st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for m in st.session_state.messages:
    cls = "bubble-assistant" if m["role"] == "model" else "bubble-user"
    pre = "⚓ EL CAPITÁN: " if m["role"] == "model" else ""
    st.markdown(f'<div class="{cls}">{pre}{m["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if prompt := st.chat_input("Hable con el Capitán..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Instrucción directa
    system = "Eres el Capitan de La Barca de San Andres. Responde en el idioma del cliente. Usa estos datos: " + carta + ". Sugiere vino Yaiza Seco."
    
    try:
        response = model.generate_content(system + "\nCliente: " + prompt)
        st.session_state.messages.append({"role": "model", "content": response.text})
        st.rerun()
    except Exception as e:
        st.error(f"Error de conexión con Google: {e}")

st.markdown("<center style='opacity:0.2; font-size:9px; color:white; margin-top:40px;'>LOCALMIND AI</center>", unsafe_allow_html=True)
