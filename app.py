import streamlit as st
from openai import OpenAI

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="La Barca de San Andrés", page_icon="⚓", layout="centered")

# --- 2. CONEXIÓN ---
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    st.error("⚠️ Error en los Secrets de Streamlit.")
    st.stop()

# --- 3. ESTÉTICA ORIGINAL (WHITE & NAVY #002147) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Helvetica+Neue:wght@300;400;600&display=swap');

    [data-testid="stAppViewContainer"] { background-color: #FFFFFF; }
    [data-testid="stMainBlockContainer"] { background-color: #FFFFFF; border-top: 5px solid #002147; padding: 20px; }

    /* BURBUJAS */
    .stChatMessage { border: 1px solid #002147; border-radius: 10px; }
    [data-testid="stChatMessageAssistant"] p { color: #002147 !important; font-weight: 500; }
    
    /* BRANDING LOCALMIND INFERIOR */
    .branding-footer { text-align: center; padding-top: 40px; border-top: 1px solid #eee; margin-top: 30px; opacity: 0.9; }
    .powered-by { color: #002147; font-size: 9px; letter-spacing: 3px; font-weight: bold; text-transform: uppercase; margin:0; }
    .localmind-logo { color: #333; font-size: 16px; font-weight: 800; margin:0; font-family: sans-serif; }
    .dot { color: #002147; }

    [data-testid="stHeader"], footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 4. SYSTEM PROMPT (EL CEREBRO DEL CAPITÁN) ---
instrucciones_base = """
Eres el asistente virtual de 'La Barca de San Andrés'. 
TU IDENTIDAD: Eres un Capitán marinero, amable y experto.
TU LEMA: Tu saludo característico es "¡Buenas, patrón!".

REGLAS DE ORO:
1. TRADUCCIÓN TOTAL: Detecta el idioma del usuario y úsalo para TODO.
2. SALUDO INTELIGENTE: Traduce tu lema "¡Buenas, patrón!" al idioma del usuario (Ej: "Hello, Captain!" en inglés, "Bonjour, patron !" en francés). NUNCA lo digas en español si el usuario habla otro idioma.
3. NO MEZCLES: Si el cliente habla alemán, no uses ninguna palabra en español o inglés.
4. RECOMENDACIONES: Sugiere siempre pescado fresco del día y vino blanco.
"""

if "messages" not in st.session_state:
    # Solo dejamos las instrucciones, el saludo lo generará la IA tras el primer mensaje
    st.session_state.messages = [{"role": "system", "content": instrucciones_base}]

# --- 5. INTERFAZ ---
st.title("⚓ La Barca de San Andrés")

# Mostrar historial (Si está vacío, mostramos un mensaje visual de bienvenida que no ensucie el chat)
if len(st.session_state.messages) <= 1:
    st.info("👋 ¡Buenas, patrón! El Capitán está listo. Pregúntele por nuestra carta en cualquier idioma.")

for m in st.session_state.messages:
    if m["role"] != "system":
        with st.chat_message(m["role"], avatar="⚓" if m["role"] == "assistant" else "👤"):
            st.markdown(m["content"])

if prompt := st.chat_input("Hable con el capitán..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"): 
        st.markdown(prompt)

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
