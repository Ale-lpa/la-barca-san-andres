import streamlit as st
from openai import OpenAI

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="La Barca de San Andrés", page_icon="⚓", layout="centered")

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    st.error("⚠️ Error en los Secrets.")
    st.stop()

# --- 2. ESTÉTICA DARK NAVY (#002147) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Helvetica+Neue:wght@300;400;600&display=swap');

    /* FONDO AZUL MARINO TOTAL */
    [data-testid="stAppViewContainer"] {
        background-color: #002147 !important;
    }
    
    [data-testid="stMainBlockContainer"] {
        background-color: rgba(0, 33, 71, 0.95) !important; /* Un poco más oscuro */
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 20px;
    }

    /* TEXTO Y BURBUJAS */
    .stChatMessage { background-color: rgba(255, 255, 255, 0.05) !important; border: 1px solid rgba(255,255,255,0.1) !important; }
    p, h1, span { color: #FFFFFF !important; }
    
    /* TEXTO ASISTENTE EN AZUL CLARO PARA DIFERENCIAR */
    [data-testid="stChatMessageAssistant"] p {
        color: #A0C4FF !important; 
        font-weight: 500;
    }

    /* BRANDING LOCALMIND */
    .branding-footer { text-align: center; padding-top: 40px; border-top: 1px solid rgba(255,255,255,0.1); margin-top: 30px; }
    .powered-by { color: #A0C4FF; font-size: 9px; letter-spacing: 3px; font-weight: bold; text-transform: uppercase; margin:0; }
    .localmind-logo { color: #fff; font-size: 16px; font-weight: 800; margin:0; font-family: sans-serif; }
    .dot { color: #A0C4FF; }

    [data-testid="stHeader"], footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. SYSTEM PROMPT (CON VENTA SUGERIDA) ---
instrucciones_base = """
Eres el asistente virtual de 'La Barca de San Andrés'. 
TU IDENTIDAD: Capitán marinero experto. 
TU LEMA: "¡Buenas, patrón!" (Tradúcelo siempre al idioma del cliente).

REGLAS DE ORO:
1. IDIOMA: Detecta y responde 100% en el idioma del usuario.
2. VENTA SUGERIDA: En CADA respuesta, sugiere acompañar la comida con un 'Vino Blanco bien frío' o 'Cerveza local'. Menciona que estas sugerencias pueden cambiar diariamente.
3. ESTILO: Tono profesional, marinero y directo.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": instrucciones_base}]

st.markdown("<h1 style='text-align: center;'>⚓ La Barca de San Andrés</h1>", unsafe_allow_html=True)

for m in st.session_state.messages:
    if m["role"] != "system":
        with st.chat_message(m["role"], avatar="⚓" if m["role"] == "assistant" else "👤"):
            st.markdown(m["content"])

if prompt := st.chat_input("Hable con el capitán..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"): st.markdown(prompt)

    with st.chat_message("assistant", avatar="⚓"):
        res_placeholder = st.empty()
        full_res = ""
        stream = client.chat.completions.create(model="gpt-4o-mini", messages=st.session_state.messages, stream=True)
        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_res += chunk.choices[0].delta.content
                res_placeholder.markdown(full_res + "▌")
        res_placeholder.markdown(full_res)
    st.session_state.messages.append({"role": "assistant", "content": full_res})

st.markdown("""<div class="branding-footer"><p class="powered-by">Powered by</p><p class="localmind-logo">Localmind<span class="dot">.</span></p></div>""", unsafe_allow_html=True)
