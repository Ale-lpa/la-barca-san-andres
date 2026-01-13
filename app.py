import streamlit as st
import json
from openai import OpenAI

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="La Barca de San Andrés | Desde 1980", page_icon="⚓", layout="centered")

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    st.error("⚠️ Error en los Secrets de OpenAI. Por favor, revísalos.")
    st.stop()

# --- 2. BASE DE DATOS REAL (Menú y Bodega) ---
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
    "Del Mar": {
        "Lomo de bacalao frito con pisto": 17.50,
        "Pata de pulpo a la brasa con patata y mojo": 19.50,
        "Calamar de potera (plancha o frito, aprox 500gr)": 18.00,
        "Pescado de lonja (según mercado)": "S/M (Consultar precio)"
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
        "Barbadillo Castillo de San Diego (Botella)": 14.00,
        "José Pariente (Verdejo) (Botella)": 22.00,
        "Pazo de Señorans (Albariño) (Botella)": 26.00
    },
    "Bodega - Vinos Tintos": {
        "Rioja Bordón Crianza (Botella)": 16.00,
        "Marqués de Riscal Reserva (Rioja)": 28.00,
        "Emilio Moro (Ribera del Duero)": 29.00,
        "Pago de Carraovejas (Ribera del Duero)": 42.00
    },
     "Bodega - Jerez y Manzanilla": {
        "Manzanilla Solear (Copa)": 3.00,
        "Tío Pepe Fino (Copa)": 3.50
    }
}

# --- 3. CSS PERSONALIZADO (LOGOS Y FONDO POSTIMAGES) ---
url_fondo = "https://i.postimg.cc/Dfs82Dv6/Gemini_Generated_Image_d7nq1bd7nq1bd7nq.png"
url_logo = "https://i.postimg.cc/dQdLqXs4/Gemini_Generated_Image_kywrxfkywrxfkywr.png"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Helvetica+Neue:wght@300;400;600&display=swap');

    /* FONDO DE IMAGEN */
    .stApp {{
        background-image: url("{url_fondo}");
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}
    
    /* CONTENEDOR DE CHAT ACLARADO */
    [data-testid="stMainBlockContainer"] {{
        background-color: rgba(255, 255, 255, 0.94) !important;
        border-radius: 20px !important;
        padding: 35px !important;
        margin-top: 25px !important;
        box-shadow: 0 10px 40px rgba(0,0,0,0.6) !important;
    }}

    /* HEADER CON LOGO DUAL */
    .header-bodega {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 20px;
        margin-bottom: 30px;
        text-align: center;
    }}
    .header-bodega img {{
        width: 70px;
        height: auto;
    }}
    .header-texto h1 {{
        margin: 0;
        font-size: 1.8rem;
        color: #002147;
        font-weight: 800;
        text-transform: uppercase;
    }}
    .header-texto p {{
        margin: 0;
        font-size: 1.1rem;
        color: #002147;
        font-weight: 500;
        letter-spacing: 2px;
    }}

    /* BURBUJAS DE CHAT */
    .stChatMessage {{ background-color: rgba(255, 255, 255, 0.5) !important; border: 1px solid #002147 !important; border-radius: 15px !important; }}
    [data-testid="stChatMessageAssistant"] p {{ color: #002147 !important; font-weight: 600; }}

    /* PIE DE PÁGINA LOCALMIND */
    .branding-footer {{ text-align: center; padding-top: 30px; border-top: 1px solid #ddd; margin-top: 30px; }}
    .powered-by {{ color: #002147; font-size: 10px; letter-spacing: 3px; font-weight: bold; text-transform: uppercase; margin:0; }}
    .localmind-logo {{ color: #333; font-size: 17px; font-weight: 800; margin:0; font-family: sans-serif; }}
    .dot {{ color: #002147; }}

    [data-testid="stHeader"], footer {{visibility: hidden;}}
    </style>
""", unsafe_allow_html=True)

# --- 4. LÓGICA DE INTELIGENCIA (SYSTEM PROMPT) ---
system_prompt = f"""
Eres el asistente virtual de 'La Barca de San Andrés', un restaurante con tradición desde 1980.
TU MENÚ REAL: {json.dumps(MENU_DB)}

INSTRUCCIONES DE ÉLITE:
1. IDIOMA: Responde 100% en el idioma que el cliente utilice.
2. TONO: Eres un Capitán amable y experto. Saluda siempre con un "¡Buenas, patrón!" (o su traducción).
3. PRECIOS: Usa siempre el símbolo '€'.
4. MARIDAJE INTELIGENTE: Varía tus recomendaciones de bodega.
   - Pescados/Entrantes -> Sugiere Blanco (José Pariente o Barbadillo) o Manzanilla Solear.
   - Carnes -> Sugiere Tintos (Emilio Moro o Rioja Bordón).
5. NO INVENTES: Si algo no está en el menú, informa de que no está disponible hoy.
"""

# --- 5. INTERFAZ DE USUARIO ---
st.markdown(f"""
    <div class="header-bodega">
        <img src="{url_logo}">
        <div class="header-texto">
            <h1>La Barca de San Andrés</h1>
            <p>DESDE 1980</p>
        </div>
        <img src="{url_logo}">
    </div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

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

# --- 6. SELLO DE CALIDAD LOCALMIND ---
st.markdown("""
<div class="branding-footer">
    <p class="powered-by">Powered by</p>
    <p class="localmind-logo">Localmind<span class="dot">.</span></p>
</div>
""", unsafe_allow_html=True)
