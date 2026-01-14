import streamlit as st
import openai

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="La Barca de San Andrés", layout="wide")

# --- 2. ESTÉTICA REFINADA (CSS ACTUALIZADO) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');
    
    /* 1. FONDO ENCUADRADO */
    .stApp {
        background-image: url("https://i.postimg.cc/Dfs82Dv6/Gemini_Generated_Image_d7nq1bd7nq1bd7nq.png");
        background-size: cover;       /* Cubre toda la pantalla sin deformar */
        background-repeat: no-repeat; /* No se repite tipo mosaico */
        background-attachment: fixed; /* Se queda fijo al hacer scroll */
        background-position: center center; /* Se centra lo mejor posible */
    }
    
    /* 3. TEXTO DEL CHAT: BLANCO CON SOMBRA OSCURA PARA LEGIBILIDAD */
    .stChatMessage [data-testid="stMarkdownContainer"] p {
        font-weight: 800 !important;
        color: #FFFFFF !important; /* Blanco puro */
        font-size: 1.15rem !important;
        line-height: 1.5 !important;
        /* Sombra negra fuerte para contraste sobre fondo claro */
        text-shadow: 2px 2px 4px rgba(0,0,0,1); 
    }

    /* Estilos de imágenes y contenedores */
    [data-testid="stImage"] img {
        max-width: 100% !important;
        height: auto !important;
        object-fit: contain !important;
    }

    .main .block-container {
        padding-bottom: 320px !important;
        padding-top: 2rem !important;
    }

    /* NOMBRE DEL COMERCIO (Solo el nombre, sin subtítulo) */
    .restaurant-title {
        font-family: 'Playfair Display', serif;
        color: #002147;
        font-size: 65px; 
        font-weight: 700;
        line-height: 0.85; 
        text-align: right;
        margin: 0;
        margin-top: 15px; /* Un poco de margen superior para centrar con el logo */
    }
    
    /* (Se ha eliminado la clase .restaurant-subtitle) */

    /* FOOTER (MARCA Y CONTACTO) */
    .sticky-footer-container {
        position: fixed;
        left: 0;
        bottom: 85px; 
        width: 100%;
        text-align: center;
        z-index: 100;
        /* Degradado más oscuro abajo para ayudar a leer el footer blanco/dorado */
        background: linear-gradient(to top, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0) 100%);
        padding-bottom: 10px;
    }

    .brand-line {
        color: #FFFFFF !important; /* Blanco para que resalte abajo */
        font-family: sans-serif;
        font-weight: 900;
        font-size: 17px;
        margin: 0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
    }
    
    .footer-link {
        color: #C5A059 !important; /* Dorado */
        text-decoration: none;
        font-weight: 900;
        font-size: 16px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. CABECERA (LOGO IZQ | NOMBRE DER) ---
col_logo, col_text = st.columns([1, 3])
with col_logo:
    st.image("https://i.imgur.com/FIn4ep3.png", width=120) 

with col_text:
    # 2. SOLO EL NOMBRE (Subtítulo eliminado)
    st.markdown("""
        <div>
            <p class="restaurant-title">La Barca de<br>San Andrés</p>
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
