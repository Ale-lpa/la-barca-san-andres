import streamlit as st
import json
from openai import OpenAI

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="La Barca de San Andrés | Desde 1980", page_icon="⚓", layout="centered")

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    st.error("⚠️ Error en los Secrets de OpenAI.")
    st.stop()

# --- 2. BASE DE DATOS COMPLETA ---
MENU_DB = {
    "Picoteo y Entrantes": {
        "Pan, picos y servicio (p.p.)": 1.50,
        "Ensaladilla de gambas y ventresca": 12.50,
        "Anchoas de Santoña 00 (6 filetes)": 16.00,
        "Salmorejo cordobés con guarnición": 10.50,
        "Tomate aliñado con melva canutera": 12.00,
        "Chocos fritos (Ración)": 14.00,
        "Adobo de cazón (Ración)": 14.00,
        "Puntillitas fritas (Ración)": 14.00,
        "Berenjenas fritas con miel de caña": 11.50,
        "Croquetas caseras del chef (8 uds)": 12.00
    },
    "Del Mar (Principales)": {
        "Lomo de bacalao frito con pisto": 17.50,
        "Pata de pulpo a la brasa con patata y mojo": 19.50,
        "Calamar de potera (aprox 500gr)": 18.00,
        "Pescado de lonja (según mercado)": "S/M (Consultar precio al patrón)"
    },
    "Carnes a la Brasa": {
        "Presa ibérica de bellota a la brasa": 19.00,
        "Solomillo de vaca madurado (aprox 250gr)": 24.00,
        "Chuletón de vaca seleccionada (al peso)": "65.00 €/kg"
    },
    "Postres Caseros": {
        "Tarta de queso al horno": 6.50,
        "Tocino de cielo con nata": 5.50,
        "Coulant de chocolate con helado": 7.00,
        "Helados variados (2 bolas)": 5.00
    },
    "Bodega - Vinos Blancos": {
        "Barbadillo Castillo de San Diego (Copa)": 3.00,
        "José Pariente (Verdejo) (Copa)": 4.50,
        "Pazo de Señorans (Albariño) (Botella)": 26.00
    },
    "Bodega - Vinos Tintos": {
        "Rioja Bordón Crianza (Copa)": 3.50,
        "Emilio Moro (Ribera del Duero) (Copa)": 5.50,
        "Marqués de Riscal Reserva (Botella)": 28.00,
        "Pago de Carraovejas (Botella)": 42.00
    },
    "Bodega - Jerez y Manzanilla": {
        "Manzanilla Solear (Copa)": 3.00,
        "Tío Pepe Fino (Copa)": 3.50
    }
}

# --- 3. CSS Y ESTÉTICA ---
url_fondo = "https://i.postimg.cc/Dfs82Dv6/Gemini_Generated_Image_d7nq1bd7nq1bd7nq.png"
url_logo = "https://i.postimg.cc/dQdLqXs4/Gemini_Generated_Image_kywrxfkywrxfkywr.png"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Playfair+Display:wght@700&display=swap');
    .stApp {{ background-image: url("{url_fondo}"); background-size: cover !important; background-attachment: fixed !important; }}
    [data-testid="stMainBlockContainer"] {{ background-color: rgba(255, 255, 255, 0.95) !important; border-radius: 25px !important; padding: 40px !important; margin-top: 20px !important; box-shadow: 0 15px 50px rgba(0,0,0,0.6) !important; }}
    .header-la-barca {{ display: flex; align-items: center; justify-content: center; gap: 25px; margin-bottom: 35px; }}
    .header-la-barca img {{ width: 90px; height: auto; }}
    .header-texto {{ display: flex; flex-direction: column; align-items: flex-end; text-align: right; }}
    .header-texto h1 {{ font-family: 'Playfair Display', serif; margin: 0; font-size: 2.4rem; color: #002147; line-height: 1.1; }}
    .header-texto .subtitle-badge {{ font-family: 'Montserrat', sans-serif; margin-top: 10px; font-size: 0.9rem; color: #002147; font-weight: 700; letter-spacing: 3px; border-top: 2px solid #002147; border-bottom: 2px solid #002147; padding: 4px 10px; }}
    .stChatMessage {{ background-color: rgba(255, 255, 255, 0.6) !important; border: 1px solid #002147 !important; border-radius: 15px !important; }}
    [data-testid="stChatMessageAssistant"] p {{ color: #002147 !important; font-weight: 600; }}
    [data-testid="stHeader"], footer {{visibility: hidden;}}
    </style>
""", unsafe_allow_html=True)

# --- 4. SYSTEM PROMPT REFORZADO ---
system_prompt = f"""
Eres el Capitán, el asistente virtual de 'La Barca de San Andrés'. 
MENU: {json.dumps(MENU_DB)}

REGLAS DE ORO (INCUMPLIRLAS ES UN ERROR CRÍTICO):
1. IDIOMA: Responde EXCLUSIVAMENTE en el mismo idioma que te hable el cliente. Si te hablan en inglés, responde en inglés. No uses el español a menos que el cliente lo haga.
2. PRECIOS COMPLETOS: Siempre que el cliente pregunte por un plato, debes dar el precio de ESE PLATO y también el precio de la BEBIDA que le recomiendes.
3. MARIDAJE POR COPA: Al sugerir vino, ofrece SIEMPRE el precio de la COPA (si está disponible en el menú) para que el cliente sienta que es una compra fácil.
4. TONO: Amable y marinero. Saluda con "¡Buenas, patrón!" (en el idioma correspondiente).
"""

# --- 5. INTERFAZ VISUAL ---
st.markdown(f"""
    <div class="header-la-barca">
        <div class="header-texto">
            <h1>La Barca de San</h1>
            <h1>Andrés</h1>
            <div class="subtitle-badge">DESDE 1980</div>
        </div>
        <img src="{url_logo}" alt="Logo Bodega">
    </div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

for m in st.session_state.messages:
    if m["role"] != "system":
        # CAMBIO DE ICONO DE USUARIO A PEZ 🐟
        avatar = "⚓" if m["role"] == "assistant" else "🐟"
        with st.chat_message(m["role"], avatar=avatar):
            st.markdown(m["content"])

if prompt := st.chat_input("Hable con el capitán..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🐟"): st.markdown(prompt)

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

# --- 6. BRANDING LOCALMIND ---
tu_numero = "34602566673" 
mensaje_wa = "Hola Alejandro, he visto el asistente de IA y me gustaría información para mi negocio."
link_whatsapp = f"https://wa.me/{tu_numero}?text={mensaje_wa.replace(' ', '%20')}"

st.markdown(f"""
<div style="text-align: center; padding-top: 35px; border-top: 1px solid #ddd; margin-top: 35px; opacity: 0.9;">
    <p style="color: #002147; font-size: 10px; letter-spacing: 3px; font-weight: bold; text-transform: uppercase; margin:0;">Powered by</p>
    <a href="{link_whatsapp}" target="_blank" style="text-decoration: none;">
        <p style="color: #333; font-size: 22px; font-weight: 800; margin:0; font-family: sans-serif;">Localmind<span style="color: #002147;">.</span></p>
    </a>
    <p style="font-size: 11px; color: #666; margin-top: 8px;">¿Quieres este asistente? <a href="{link_whatsapp}" target="_blank" style="color: #002147; font-weight: bold;">Contacta con nosotros</a></p>
</div>
""", unsafe_allow_html=True)
