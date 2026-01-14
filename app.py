import streamlit as st
import openai

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="La Barca de San Andrés", layout="wide")

# --- 2. ESTÉTICA REFINADA (SOLUCIÓN FINAL AL LOGO) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');
    
    /* FONDO FIJO */
    .stApp {
        background-image: url("https://i.postimg.cc/Dfs82Dv6/Gemini_Generated_Image_d7nq1bd7nq1bd7nq.png");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center center;
    }
    
    /* ELIMINAR MÁRGENES SUPERIORES E INFERIORES POR DEFECTO */
    .block-container {
        padding-top: 1rem !important; /* Un poco de aire arriba para que no se corte nada */
        padding-bottom: 200px !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    /* TEXTO DEL CHAT: BLANCO CON SOMBRA */
    .stChatMessage [data-testid="stMarkdownContainer"] p {
        font-weight: 800 !important;
        color: #FFFFFF !important;
        font-size: 1.15rem !important;
        line-height: 1.5 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,1); 
    }

    /* --- CABECERA PERFECTA --- */

    /* 1. TÍTULO: ALINEADO ARRIBA A LA DERECHA */
    .header-right-box {
        text-align: right;
        width: 100%;
        margin-top: -30px; /* Ajuste suave para subirlo sin que se salga */
    }

    .restaurant-title {
        font-family: 'Playfair Display', serif;
        color: #002147;
        font-size: 65px; 
        font-weight: 700;
        line-height: 0.85; 
        margin: 0;
    }
    
    /* SUBTÍTULO LEGIBLE CON SOMBRA */
    .restaurant-subtitle {
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
    }

    /* 2. LOGO: ENCAJADO EN LA ESQUINA SIN CORTES */
    .logo-left-box {
        margin-top: -25px; /* Sube el logo para emparejarlo visualmente con el título */
        margin-left: -10px; /* Lo pega un poco más a la izquierda */
        text-align: left;
    }
    
    /* Asegurar que la imagen no se recorte */
    [data-testid="stImage"] {
        overflow: visible !important;
    }

    /* --- RESTO DE ESTILOS --- */

    [data-testid="stChatInput"] {
        border-top: none !important;
        box-shadow: none !important;
    }
    .stChatInputContainer {
        padding-bottom: 20px !important;
        background-color: transparent !important;
    }

    .sticky-footer-container {
        position: fixed;
        left: 0;
        bottom: 95px; 
        width: 100%;
        text-align: center;
        z-index: 100;
        background: linear-gradient(to top, rgba(255,255,255,0.4) 0%, rgba(255,255,255,0) 100%);
        padding-bottom: 5px;
    }

    .brand-line {
        color: #FFFFFF !important;
        font-family: sans-serif;
        font-weight: 900;
        font-size: 17px;
        margin: 0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
    }
    
    .footer-link {
        color: #C5A059 !important;
        text-decoration: none;
        font-weight: 900;
        font-size: 16px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. CABECERA (COLUMNAS AJUSTADAS) ---
# Damos un poco más de espacio a la columna del logo para que respire
col_logo, col_text = st.columns([1.2, 2.8]) 
with col_logo:
    # Logo encajado
    st.markdown('<div class="logo-left-box">', unsafe_allow_html=True)
    st.image("https://i.imgur.com/FIn4ep3.png", width=120)
    st.markdown('</div>', unsafe_allow_html=True)

with col_text:
    # Título alineado
    st.markdown("""
        <div class="header-right-box">
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

MENÚ PRINCIPAL:
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

# --- 5. LÓGICA DE CHAT CON STREAMING ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    icon = "🐟" if message["role"] == "user" else "⚓"
    with st.chat_message(message["role"], avatar=icon):
        st.markdown(message["content"])

if prompt := st.chat_input("Hable con el capitán..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🐟"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="⚓"):
        contexto_chat = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        
        stream = client.chat.completions.create(
            model="gpt-4",
            messages=contexto_chat,
            temperature=0.7,
            stream=True 
        )
        full_response = st.write_stream(stream)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- 6. PIE DE PÁGINA ---
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
