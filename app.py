import streamlit as st

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="La Barca de San Andrés", layout="wide")

# --- ESTÉTICA COMPLETA (CSS) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&display=swap');
    
    /* Imagen de fondo */
    .stApp {{
        background-image: url("https://i.postimg.cc/Dfs82Dv6/Gemini_Generated_Image_d7nq1bd7nq1bd7nq.png");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Contenedor principal para legibilidad */
    .block-container {{
        background: rgba(255, 255, 255, 0.92); /* Fondo blanco semi-transparente para leer bien */
        padding: 2rem;
        border-radius: 20px;
        margin-top: 2rem;
    }}

    /* Título principal "TOP" (Sin espacios) */
    .main-title {{
        font-family: 'Playfair Display', serif;
        color: #00264d;
        font-size: 45px;
        font-weight: 800;
        line-height: 0.85; 
        margin: 0;
        padding: 0;
    }}

    .subtitle-box {{
        display: inline-block;
        border-top: 2px solid #00264d;
        border-bottom: 2px solid #00264d;
        margin-top: 10px;
        padding: 4px 15px;
    }}

    .subtitle-text {{
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 14px;
        letter-spacing: 4px;
        color: #b08d57;
        font-weight: bold;
        margin: 0;
    }}

    /* Footer y Botón WhatsApp */
    .footer-text {{
        text-align: center;
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 14px;
        color: #666;
        margin-top: 50px;
    }}
    
    .whatsapp-button {{
        display: block;
        width: 200px;
        margin: 20px auto;
        padding: 10px;
        background-color: #25d366;
        color: white;
        text-align: center;
        border-radius: 10px;
        text-decoration: none;
        font-weight: bold;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
col1, col2 = st.columns([0.7, 0.3])

with col1:
    st.markdown("""
        <div class="main-title">
            La Barca<br>de San<br>Andrés
        </div>
        <div class="subtitle-box">
            <p class="subtitle-text">DESDE 1980</p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    # Nuevo Logo
    st.image("https://i.postimg.cc/dQdLqXs4/Gemini_Generated_Image_kywrxfkywrxfkywr.png", width=120)

st.markdown("<br>", unsafe_allow_html=True)

# --- MENÚ COMPLETO (BASE DE DATOS JSON) ---
menu_json = {
    "entrantes": [
        {"plato": "Papas arrugadas con mojo canario", "precio": 5.50, "maridaje": "Yaiza Seco"},
        {"plato": "Gofio escaldado con cebolla roja", "precio": 5.80, "maridaje": "Mencey Chasna Seco"},
        {"plato": "Gambas al ajillo", "precio": 12.50, "maridaje": "Jose Pariente"},
        {"plato": "Pulpo a la carmela", "precio": 20.50, "maridaje": "Martinon Blanc de Noir"},
        {"plato": "Queso herreño a la plancha", "precio": 10.50, "maridaje": "Mencey Chasna Afrutado"},
        {"plato": "Lapas a la carmela", "precio": 10.50, "maridaje": "Yaiza Seco"}
    ],
    "carnes": [
        {"plato": "Solomillo al grill", "precio": 22.90, "maridaje": "Ramon Bilbao Crianza"},
        {"plato": "Chuleton de vaca rubia gallega", "precio": 55.00, "unidad": "kg", "maridaje": "Pago de Carraovejas"}
    ],
    "pescados_y_mariscos": [
        {"plato": "Pescado fresco del pais", "precio": 38.00, "unidad": "kg", "maridaje": "Martinon Seco"},
        {"plato": "Bogavante a la plancha", "precio": 95.00, "unidad": "kg", "maridaje": "Veuve Clicquot"}
    ],
    "arroces": [
        {"plato": "Arroz caldoso de bogavante", "precio": 64.00, "maridaje": "Jose Pariente Barrica"}
    ]
}

# --- PROMPT DEL SISTEMA ---
prompt_sistema = f"""
Actúa como el sumiller experto de 'La Barca de San Andrés'. 
Consulta este menú para responder: {menu_json}
REGLAS:
1. Responde en el idioma del cliente.
2. Cada plato debe ir con su PRECIO y su MARIDAJE.
3. Sé directo y profesional.
"""

# --- INTERFAZ DE CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if input_usuario := st.chat_input("Hable con el capitán..."):
    st.session_state.messages.append({"role": "user", "content": input_usuario})
    with st.chat_message("user"):
        st.markdown(input_usuario)

    with st.chat_message("assistant"):
        # La IA aquí generará la respuesta basándose en el prompt_sistema
        respuesta = "Nuestro sumiller le recomienda el **Bogavante a la plancha (95,00€/kg)** maridado con un **Champagne Veuve Clicquot** para una experiencia inigualable."
        st.markdown(respuesta)
        st.session_state.messages.append({"role": "assistant", "content": respuesta})

# --- PIE DE PÁGINA Y CONTACTO ---
st.markdown("""
    <div class="footer-text">
        <p>Powered by <b>Localmind.</b></p>
        <a href="https://wa.me/TU_NUMERO_AQUI" class="whatsapp-button">Reserva por WhatsApp</a>
    </div>
    """, unsafe_allow_html=True)
