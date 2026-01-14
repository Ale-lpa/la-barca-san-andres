import streamlit as st
import openai

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="La Barca de San Andrés", layout="wide")

# --- 2. ESTÉTICA REFINADA (CSS TOTAL) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');
    
    /* Fondo fijo */
    .stApp {
        background-image: url("https://i.postimg.cc/Dfs82Dv6/Gemini_Generated_Image_d7nq1bd7nq1bd7nq.png");
        background-size: cover;
        background-attachment: fixed;
        background-position: center center;
    }
    
    /* 4. COLOR AZUL CORPORATIVO Y NEGRITA (Selector profundo) */
    .stChatMessage [data-testid="stMarkdownContainer"] p {
        font-weight: 800 !important;
        color: #002147 !important;
        font-size: 1.15rem !important;
        line-height: 1.5 !important;
    }

    /* 2. LOGO SIN RECORTES */
    [data-testid="stImage"] img {
        max-width: 100% !important;
        height: auto !important;
        object-fit: contain !important;
    }

    /* ESTILO DEL NOMBRE (A la derecha) */
    .restaurant-title {
        font-family: 'Playfair Display', serif;
        color: #002147;
        font-size: 65px; 
        font-weight: 700;
        line-height: 0.85; 
        text-align: right;
        margin: 0;
    }
    .restaurant-subtitle {
        color: #C5A059;
        letter-spacing: 5px;
        font-size: 16px;
        font-weight: bold;
        border-top: 2px solid #002147;
        display: inline-block;
        margin-top: 10px;
        padding-top: 5px;
        text-transform: uppercase;
        float: right;
    }

    /* 3. FOOTER FIJO SIN SOLAPAMIENTO */
    .sticky-footer-container {
        position: fixed;
        left: 0;
        bottom: 85px; /* Ajustado para estar sobre el input */
        width: 100%;
        text-align: center;
        z-index: 100;
        background: linear-gradient(to top, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0) 100%);
        padding-bottom: 10px;
    }

    .brand-line {
        color: #002147 !important;
        font-family: sans-serif;
        font-weight: 900;
        font-size: 17px;
        margin: 0;
    }
    
    .footer-link {
        color: #C5A059 !important;
        text-decoration: none;
        font-weight: 900;
        font-size: 16px;
    }

    /* Límite de chat para que no baje más de la cuenta */
    .main .block-container {
        padding-bottom: 300px !important;
        padding-top: 2rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. CABECERA (LOGO IZQ | NOMBRE DER) ---
col_logo, col_text = st.columns([1, 3])
with col_logo:
    # Logo ajustado
    st.image("https://i.imgur.com/FIn4ep3.png", width=120) 

with col_text:
    st.markdown("""
        <div>
            <p class="restaurant-title">La Barca de<br>San Andrés</p>
            <p class="restaurant-subtitle">desde 1980</p>
        </div>
    """, unsafe_allow_html=True)

# --- 4. SYSTEM PROMPT ---
SYSTEM_PROMPT = """
Eres el sumiller virtual de 'La Barca de San Andrés'. 
REGLAS:
1. IDIOMA: Responde en el idioma del cliente.
2. NO REPETICIÓN: Ofrece siempre opciones nuevas.
3. MARIDAJE TOTAL: Indica PRECIO y VINO sugerido por cada plato.

MENÚ:
- Papas arrugadas (5,50€): Yaiza Seco.
- Gofio escaldado (5,80€): Mencey Chasna Seco.
- Gambas al ajillo (12,50€): Jose Pariente.
- Pulpo a la Carmela (20,50€): Martinón Blanc de Noir.
- Chuletón Vaca Rubia (55€/kg): Pago de Carraovejas.
- Pescado fresco (38€/kg): Martinón Seco.
- Lapas con mojo (10,50€): Yaiza Seco.
- Arroz Caldoso Bogavante (64€): Jose Pariente Barrica.
- Polvito Uruguayo (5,50€): Yaiza Afrutado.

Contacto: WhatsApp 602566673. Asistente: 'Powered by Localmind'.
"""

# --- 5. LÓGICA DE CHAT CON ANIMACIÓN (STREAMING) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Historial
for message in st.session_state.messages:
    icon = "🐟" if message["role"] == "user" else "⚓"
    with st.chat_message(message["role"], avatar=icon):
        st.markdown(message["content"])

# Entrada de chat
if prompt := st.chat_input("Hable con el capitán..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🐟"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="⚓"):
        contexto_chat = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        
        # 1. ANIMACIÓN DE ESCRITURA ACTIVADA
        stream = client.chat.completions.create(
            model="gpt-4",
            messages=contexto_chat,
            temperature=0.7,
            stream=True # Activa el flujo de datos
        )
        
        # Mostramos la respuesta mientras se genera
        full_response = st.write_stream(stream)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- 6. PIE DE PÁGINA (BRANDING Y CONTACTO) ---
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
