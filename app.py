import streamlit as st
from openai import OpenAI

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="La Barca de San Andrés | Asistente", page_icon="⚓", layout="centered")

# --- 2. CONEXIÓN ---
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    st.error("⚠️ Configuración de API incompleta.")
    st.stop()

# --- 3. DISEÑO PREMIUM (AZUL MARINO REAL #002147) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Helvetica+Neue:wght@300;400;600&display=swap');

    [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF;
        background-image: radial-gradient(#002147 0.5px, transparent 0.5px);
        background-size: 30px 30px;
    }
    
    [data-testid="stMainBlockContainer"] {
        background-color: rgba(255, 255, 255, 0.95);
        border-top: 5px solid #002147;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }

    /* ESTILO DE BURBUJAS */
    [data-testid="stChatMessageAssistant"] {
        background-color: #f0f4f8 !important;
        border-left: 5px solid #002147 !important;
    }
    [data-testid="stChatMessageAssistant"] p {
        color: #002147 !important;
        font-weight: 500;
    }

    /* BRANDING LOCALMIND AL FINAL */
    .branding-footer { text-align: center; padding-top: 30px; border-top: 1px solid #eee; margin-top: 30px; }
    .powered-by { color: #002147; font-size: 9px; letter-spacing: 3px; font-weight: bold; text-transform: uppercase; margin:0; }
    .localmind-logo { color: #333; font-size: 16px; font-weight: 800; margin:0; font-family: sans-serif; }
    .dot { color: #002147; }

    [data-testid="stHeader"], footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 4. SYSTEM PROMPT (LA REGLA DE ORO) ---
instrucciones_base = """
Eres el asistente virtual de 'La Barca de San Andrés'. 
TU TONO: Marinero, amable, tradicional y servicial. Saludas con un '¡Buenas, patrón!' o similar.
REGLA DE ORO DE IDIOMA:
1. Detecta el idioma del usuario inmediatamente.
2. Responde ÚNICA Y EXCLUSIVAMENTE en ese idioma.
3. Prohibido mezclar idiomas. Si hablan en inglés, todo en inglés.
RECOMENDACIONES: Siempre prioriza pescados frescos de la zona y vinos blancos fríos.
"""

# --- 5. LÓGICA DEL CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": instrucciones_base}]

# Header Visual
st.title("⚓ La Barca de San Andrés")
st.caption("Tradición marinera con inteligencia artificial")

# Historial
for m in st.session_state.messages:
    if m["role"] != "system":
        with st.chat_message(m["role"], avatar="⚓" if m["role"] == "assistant" else "👤"):
            st.markdown(m["content"])

# Input y Streaming
if prompt := st.chat_input("¿Qué desea degustar hoy?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"): st.markdown(prompt)

    with st.chat_message("assistant", avatar="⚓"):
        res_placeholder = st.empty()
        full_res = ""
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages,
            stream=True
        )
        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_res += chunk.choices[0].delta.content
                res_placeholder.markdown(full_res + "▌")
        res_placeholder.markdown(full_res)
    
    st.session_state.messages.append({"role": "assistant", "content": full_res})

# --- 6. BRANDING LOCALMIND ---
st.markdown("""
<div class="branding-footer">
    <p class="powered-by">Powered by</p>
    <p class="localmind-logo">Localmind<span class="dot">.</span></p>
</div>
""", unsafe_allow_html=True)
