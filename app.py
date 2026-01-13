import streamlit as st
import json
from openai import OpenAI

# --- 1. CONFIGURACIÓN ---
# Nota: El icono de la pestaña sigue siendo el ancla por limitaciones técnicas de Streamlit
st.set_page_config(page_title="La Barca de San Andrés | Desde 1980", page_icon="⚓", layout="centered")

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    st.error("⚠️ Error en los Secrets de Streamlit.")
    st.stop()

# --- 2. BASE DE DATOS REAL (Extraída del Menú) ---
MENU_DB = {
    "Picoteo y Entrantes": {
        "Pan, picos y servicio (p.p.)": 1.50,
        "Ensaladilla de gambas y ventresca": 12.50,
        "Anchoas de Santoña 00 (6 filetes)": 16,00,
        "Salmorejo cordobés con guarnición": 10.50,
        "Tomate aliñado con melva canutera": 12.00,
        "Chocos fritos (Ración)": 14.00,
        "Adobo de cazón (Ración)": 14.00,
        "Puntillitas fritas (Ración)": 14.00,
        "Berenjenas fritas con miel de caña": 11.50,
        "Croquetas caseras del chef (8 uds)": 12.00
    },
    "Del Mar (Platos Principales)": {
        "Lomo de bacalao frito con pisto": 17.50,
        "Pata de pulpo a la brasa con patata y mojo": 19.50,
        "Calamar de potera (plancha o frito, aprox 500gr)": 18.00,
        "Pescado de lonja (según mercado)": "S/M (Consultar precio)"
    },
    "Carnes a la Brasa": {
        "Presa ibérica de bellota a la brasa": 19.00,
        "Solomillo de vaca madurado (aprox 250gr)": 24.00,
        "Chuletón de vaca seleccionada (al peso)": "65,00 €/kg"
    },
    "Postres Caseros": {
        "Tarta de queso al horno": 6.50,
        "Tocino de cielo con nata": 5.50,
        "Coulant de chocolate con helado": 7.00,
        "Helados variados (2 bolas)": 5.00
    },
    "Bodega - Vinos Blancos": {
        "Barbadillo Castillo de San Diego (Cádiz) - Botella": 14.00,
        "Barbadillo Castillo de San Diego (Cádiz) - Copa": 3.00,
        "José Pariente (Rueda Verdejo) - Botella": 22.00,
        "José Pariente (Rueda Verdejo) - Copa": 4.50,
        "Pazo de Señorans (Rías Baixas Albariño) - Botella": 26.00
    },
    "Bodega - Vinos Tintos": {
        "Rioja Bordón Crianza - Botella": 16.00,
        "Rioja Bordón Crianza - Copa": 3.50,
        "Marqués de Riscal Reserva (Rioja) - Botella": 28.00,
        "Emilio Moro (Ribera del Duero) - Botella": 29.00,
        "Emilio Moro (Ribera del Duero) - Copa": 5.50,
        "Pago de Carraovejas (Ribera del Duero) - Botella": 42.00
    },
     "Bodega - Jerez y Manzanilla": {
        "Manzanilla Solear (Copa)": 3.00,
        "Tío Pepe Fino (Copa)": 3.50
    }
}

# --- 3. CSS PERSONALIZADO (FONDO Y LOGOTIPOS) ---
# ¡ATENCIÓN ALEJANDRO! SUSTITUYE LAS URLs DE ABAJO POR LAS TUYAS REALES
url_fondo = “https://imgur.com/a/Sny0MDp”
url_logo = "https://imgur.com/a/7kn9qlC"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Helvetica+Neue:wght@300;400;600&display=swap');

    /* FONDO DE MADERA AZUL */
    [data-testid="stAppViewContainer"] {{
        background-image: url('{url_fondo}') !important;
        background-size: cover !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
    }}
    
    /* CONTENEDOR PRINCIPAL CON FONDO BLANCO TRANSLÚCIDO */
    [data-testid="stMainBlockContainer"] {{
        background-color: rgba(255, 255, 255, 0.92) !important;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }}

    /* ESTILO DEL TÍTULO PERSONALIZADO */
    .titulo-bodega {{
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Helvetica Neue', serif;
        color: #002147; /* Azul marino del logo */
        margin-bottom: 20px;
    }}
    .titulo-bodega img {{
        height: 60px; /* Tamaño del logo */
        margin: 0 15px;
    }}
    .titulo-texto {{
        text-align: center;
    }}
    .titulo-texto h1 {{ margin: 0; font-size: 2rem; font-weight: 700; }}
    .titulo-texto p {{ margin: 0; font-size: 1rem; opacity: 0.8; }}

    /* BURBUJAS DE CHAT ESTILO MARINERO */
    .stChatMessage {{ background-color: rgba(240, 244, 248, 0.9) !important; border: 1px solid #002147 !important; }}
    [data-testid="stChatMessageAssistant"] p {{ color: #002147 !important; font-weight: 600; }}

    /* BRANDING LOCALMIND */
    .branding-footer {{ text-align: center; padding-top: 30px; border-top: 1px solid #ccc; margin-top: 30px; }}
    .powered-by {{ color: #002147; font-size: 9px; letter-spacing: 3px; font-weight: bold; text-transform: uppercase; margin:0; }}
    .localmind-logo {{ color: #333; font-size: 16px; font-weight: 800; margin:0; font-family: sans-serif; }}
    .dot {{ color: #002147; }}

    [data-testid="stHeader"], footer {{visibility: hidden;}}
    </style>
""", unsafe_allow_html=True)

# --- 4. SYSTEM PROMPT (RECOMENDACIONES VARIADAS) ---
system_prompt = f"""
Eres el asistente virtual de 'La Barca de San Andrés' (fundada en 1980).
TU MENÚ REAL: {json.dumps(MENU_DB)}

REGLAS DE ORO:
1. IDIOMA Y TONO: Responde 100% en el idioma del cliente. Usa un tono amable, tradicional y marinero ("¡Buenas, patrón!").
2. PRECIOS: Muestra SIEMPRE '€' junto a cada precio. Si es S/M o al peso, indícalo claramente.
3. VENTA SUGERIDA INTELIGENTE: Cuando pidan comida, sugiere UNA bebida que maride bien. ¡VARÍA! No sugieras siempre lo mismo.
    - Si piden pescado/marisco -> Sugiere vinos blancos (Barbadillo, Albariño, etc.).
    - Si piden carne -> Sugiere vinos tintos (Rioja, Ribera).
    - Si piden entrantes/fritura -> Sugiere Manzanilla o Fino bien frío.
4. NO INVENTES: Cíñete estrictamente al menú proporcionado.
"""

# --- 5. INTERFAZ CON TÍTULO PERSONALIZADO ---
# Usamos HTML para insertar los logos exactamente como pediste
st.markdown(f"""
    <div class="titulo-bodega">
        <img src="{url_logo}" alt="Logo Bodega La Barca">
        <div class="titulo-texto">
            <h1>La Barca de San Andrés</h1>
            <p>Desde 1980</p>
        </div>
        <img src="{url_logo}" alt="Logo Bodega La Barca">
    </div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

for m in st.session_state.messages:
    if m["role"] != "system":
        # Usamos el ancla para el chat, ya que el logo está en el título
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

# --- 6. BRANDING LOCALMIND ---
st.markdown("""<div class="branding-footer"><p class="powered-by">Powered by</p><p class="localmind-logo">Localmind<span class="dot">.</span></p></div>""", unsafe_allow_html=True)
