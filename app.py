import streamlit as st
import openai

# --- 1. CONFIGURACIÓN DE IDENTIDAD (PARA TUS DEMOS) ---
NOMBRE_RESTAURANTE = "Nombre de<br>Tu Local" 
ESLOGAN = "SABOR Y TRADICIÓN"
# Usamos un logo transparente o el de LocalMind para evitar el error negro
LOGO_URL = "https://i.postimg.cc/mD78698X/localmind-logo.png" 

# --- 2. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Asistente IA - LocalMind", layout="wide")

# --- 3. ESTÉTICA REFINADA ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');
    
    /* FONDO NÁUTICO */
    .stApp {{
        background-image: url("https://i.postimg.cc/Dfs82Dv6/Gemini_Generated_Image_d7nq1bd7nq1bd7nq.png");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center center;
    }}
    
    .block-container {{
        padding-top: 0rem !important;
        padding-bottom: 220px !important; /* Espacio para el footer elevado */
        padding-left: 0rem !important;  
        padding-right: 0rem !important; 
        max-width: 100% !important;
    }}

    /* ELIMINAR TEXTO DE ERROR DE IMAGEN (ARRIBA IZQUIERDA) */
    [data-testid="stImage"] div {{
        color: transparent !important;
        font-size: 0px !important;
    }}
    [data-testid="stImage"] img {{
        background: transparent !important;
    }}

    /* TEXTO DEL CHAT */
    .stChatMessage [data-testid="stMarkdownContainer"] p {{
        font-weight: 800 !important;
        color: #FFFFFF !important;
        font-size: 1.15rem !important;
        line-height: 1.5 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,1); 
    }}

    /* CABECERA IZQUIERDA (LOGO) */
    .logo-container {{
        position: absolute;
        left: 0.5rem !important;
        top: 35px; 
        z-index: 100;
    }}

    /* CABECERA DERECHA (TÍTULO) */
    .header-right-box {{
        text-align: right;
        width: 100%;
        margin-top: -125px; 
        padding-right: 15px; 
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
        font-weight: 900 !important;
        border-top: 2px solid #002147;
        display: inline-block;
        margin-top: 5px;
        padding-top: 5px;
        text-transform: uppercase;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
    }}

    /* AJUSTES DE INPUT */
    [data-testid="stChatInput"] {{ border-top: none !important; box-shadow: none !important; }}
    .stChatInputContainer {{ background-color: transparent !important; padding-bottom: 20px !important; }}

    /* FOOTER ELEVADO PARA VISIBILIDAD TOTAL */
    .sticky-footer-container {{
        position: fixed; 
        left: 0; 
        bottom: 115px; /* Subido de 95px para que se vea bien */
        width: 100%; 
        text-align: center; 
        z-index: 100;
        background: linear-gradient(to top, rgba(255,255,255,0.4) 0%, rgba(255,255,255,0) 100%);
        padding-bottom: 10px;
    }}

    .brand-line {{ 
        color: #FFFFFF !important; 
        font-family: sans-serif; 
        font-weight: 900; 
        font-size: 16px; 
        margin: 0; 
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8); 
    }}

    .footer-link {{ 
        color: #C5A059 !important; 
        text-decoration: none; 
        font-weight: 900; 
        font-size: 15px; 
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8); 
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. CABECERA ---
col_logo, col_text = st.columns([1, 3])
with col_logo:
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    st.image(LOGO_URL, width=110)
    st.markdown('</div>', unsafe_allow_html=True)

with col_text:
    st.markdown(f"""
        <div class="header-right-box">
            <p class="restaurant-title">{NOMBRE_RESTAURANTE}</p>
            <p class="restaurant-subtitle">{ESLOGAN}</p>
        </div>
    """, unsafe_allow_html=True)

# --- 5. LÓGICA DE ASISTENTE ---
SYSTEM_PROMPT = f"Eres el sumiller virtual de {NOMBRE_RESTAURANTE}. REGLAS: 1. Responde en el idioma del cliente. 2. Indica PRECIO y VINO sugerido por cada plato. Usa un tono experto y amable."

if "messages" not in st.session_state: st.session_state.messages = []
for message in st.session_state.messages:
    icon = "🐟" if message["role"] == "user" else "⚓"
    with st.chat_message(message["role"], avatar=icon): st.markdown(message["content"])

if prompt := st.chat_input("Hable con el asistente..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🐟"): st.markdown(prompt)
    with st.chat_message("assistant", avatar="⚓"):
        contexto = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        stream = client.chat.completions.create(model="gpt-4o", messages=contexto, temperature=0.7, stream=True)
        full_response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- 6. PIE DE PÁGINA (BRANDING Y WHATSAPP) ---
st.markdown(f"""
    <div class="sticky-footer-container">
        <p class="brand-line">powered by localmind.</p>
        <p>
            <a href="https://wa.me/34602566673" target="_blank" class="footer-link">
                ¿Quieres este asistente?
            </a>
        </p>
    </div>
""", unsafe_allow_html=True)
