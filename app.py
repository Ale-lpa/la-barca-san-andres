import streamlit as st
import openai

# --- 1. CONFIGURACIÓN DE IDENTIDAD ---
NOMBRE_RESTAURANTE = "Nombre de<br>Tu Local" 
ESLOGAN = "SABOR Y TRADICIÓN"
# DEJA ESTO VACÍO ( "" ) si no tienes logo todavía para que no de error
LOGO_URL = "" 

# --- 2. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Asistente IA - LocalMind", layout="wide")

# --- 3. ESTÉTICA REFINADA (SIN ERRORES VISUALES) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');
    
    .stApp {{
        background-image: url("https://i.postimg.cc/Dfs82Dv6/Gemini_Generated_Image_d7nq1bd7nq1bd7nq.png");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center center;
    }}
    
    .block-container {{
        padding-top: 0rem !important;
        padding-bottom: 230px !important;
        max-width: 100% !important;
    }}

    /* OCULTAR EL CONTENEDOR DE IMAGEN SI HAY ERROR */
    [data-testid="stImage"] {{
        background: transparent !important;
    }}
    [data-testid="stImage"] [data-testid="stMarkdownContainer"] {{
        display: none !important;
    }}

    /* TEXTO DEL CHAT */
    .stChatMessage [data-testid="stMarkdownContainer"] p {{
        font-weight: 800 !important;
        color: #FFFFFF !important;
        font-size: 1.15rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,1); 
    }}

    /* CABECERA IZQUIERDA (LOGO) */
    .logo-container {{
        position: absolute;
        left: 15px !important;
        top: 35px; 
        z-index: 100;
    }}

    /* CABECERA DERECHA (TÍTULO) */
    .header-right-box {{
        text-align: right;
        width: 100%;
        margin-top: -125px; 
        padding-right: 20px; 
    }}

    .restaurant-title {{
        font-family: 'Playfair Display', serif;
        color: #002147;
        font-size: 60px; 
        font-weight: 700;
        line-height: 0.85; 
        margin: 0;
    }}
    
    .restaurant-subtitle {{
        color: #C5A059;
        letter-spacing: 5px;
        font-size: 16px;
        font-weight: 900;
        border-top: 2px solid #002147;
        display: inline-block;
        margin-top: 5px;
        padding-top: 5px;
        text-transform: uppercase;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
    }}

    /* FOOTER Y WHATSAPP */
    .sticky-footer-container {{
        position: fixed; 
        left: 0; 
        bottom: 115px; 
        width: 100%; 
        text-align: center; 
        z-index: 100;
        background: linear-gradient(to top, rgba(255,255,255,0.5) 0%, rgba(255,255,255,0) 100%);
    }}

    .brand-line {{ color: #FFFFFF !important; font-weight: 900; font-size: 16px; text-shadow: 1px 1px 2px rgba(0,0,0,0.8); }}
    .footer-link {{ color: #C5A059 !important; text-decoration: none; font-weight: 900; text-shadow: 1px 1px 2px rgba(0,0,0,0.8); }}
    </style>
""", unsafe_allow_html=True)

# --- 4. CABECERA (SOLO PINTA LOGO SI EXISTE URL) ---
col_logo, col_text = st.columns([1, 3])
with col_logo:
    if LOGO_URL:
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        st.image(LOGO_URL, width=115)
        st.markdown('</div>', unsafe_allow_html=True)

with col_text:
    st.markdown(f"""
        <div class="header-right-box">
            <p class="restaurant-title">{NOMBRE_RESTAURANTE}</p>
            <p class="restaurant-subtitle">{ESLOGAN}</p>
        </div>
    """, unsafe_allow_html=True)

# --- 5. LÓGICA DE ASISTENTE CON ESCRITURA RÁPIDA ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Dibujar historial previo
for message in st.session_state.messages:
    icon = "🐟" if message["role"] == "user" else "⚓"
    with st.chat_message(message["role"], avatar=icon):
        st.markdown(message["content"])

# Nuevo mensaje
if prompt := st.chat_input("Hable con el asistente..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🐟"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="⚓"):
        contexto = [{"role": "system", "content": f"Eres el sumiller virtual de {NOMBRE_RESTAURANTE}. Responde en el idioma del cliente con precios y maridajes."}] + st.session_state.messages
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        
        # El streaming=True es lo que activa el envío de datos por trozos
        stream = client.chat.completions.create(
            model="gpt-4o", 
            messages=contexto, 
            stream=True
        )
        
        # write_stream es la función que hace la animación de escritura
        full_response = st.write_stream(stream)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- 6. PIE DE PÁGINA ---
st.markdown(f"""
    <div class="sticky-footer-container">
        <p class="brand-line">powered by localmind.</p>
        <p><a href="https://wa.me/34602566673" target="_blank" class="footer-link">¿Quieres este asistente?</a></p>
    </div>
""", unsafe_allow_html=True)
