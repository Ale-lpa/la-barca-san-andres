import streamlit as st
import openai

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="La Barca de San Andrés", layout="wide")

# --- 2. ESTÉTICA REFINADA (CSS CON NUEVO FONDO) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');
    
    /* NUEVO FONDO FIJO (Barca en la playa) */
    .stApp {
        background-image: url("https://i.imgur.com/SrelLXf.jpeg");
        background-size: cover;
        background-attachment: fixed;
        background-position: center center;
    }
    
    /* 1. TEXTO DEL CHAT: NEGRO INTENSO Y MÁXIMO GROSOR */
    .stChatMessage [data-testid="stMarkdownContainer"] p {
        font-weight: 900 !important; 
        color: #000000 !important; /* Negro puro intenso */
        font-size: 1.15rem !important;
        line-height: 1.5 !important;
        text-shadow: 0px 1px 1px rgba(255,255,255,0.8); /* Sombra blanca fuerte para leer sobre fondo oscuro */
    }

    /* NOMBRE DEL COMERCIO (A la derecha) */
    .restaurant-title {
        font-family: 'Playfair Display', serif;
        color: #002147;
        font-size: 65px; 
        font-weight: 700;
        line-height: 0.85; 
        text-align: right;
        margin: 0;
        /* Sombra blanca al título también para que resalte en el cielo */
        text-shadow: 2px 2px 4px rgba(255,255,255,0.8); 
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
        background-color: rgba(255,255,255,0.7); /* Fondo sutil para el subtítulo */
        padding-left: 10px;
        padding-right: 10px;
    }

    /* 3. FOOTER (MARCA Y CONTACTO) */
    .sticky-footer-container {
        position: fixed;
        left: 0;
        bottom: 85px; 
        width: 100%;
        text-align: center;
        z-index: 100;
        /* Fondo blanco más opaco para leer bien el pie sobre la arena */
        background: linear-gradient(to top, rgba(255,255,255,0.9) 20%, rgba(255,255,255,0) 100%);
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

    /* MARGEN DE SEGURIDAD PARA EL CHAT */
    .main .block-container {
        padding-bottom: 320px !important;
        padding-top: 2rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. CABECERA (SOLO NOMBRE A LA DERECHA, SIN LOGO) ---
# Se han eliminado las columnas y la imagen del logo
st.markdown("""
    <div style="width: 100%; text-align: right;">
        <p class="restaurant-title">La Barca de<br>San Andrés</p>
        <p class="restaurant-subtitle">desde 1980</p>
    </div>
""", unsafe_allow_html=True)

# --- 4. SYSTEM PROMPT ---
SYSTEM_PROMPT = """
Eres el sumiller virtual de 'La Barca de San Andrés'. 
REGLAS:
1. IDIOMA: Responde en el idioma del cliente.
2. NO REPETICIÓN: Ofrece siempre opciones nuevas de la carta.
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

# Historial con iconos personalizados
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
        
        # Generación con flujo de datos (Animación)
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
