import streamlit as st

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="La Barca de San Andrés", layout="wide")

# --- ESTÉTICA FINAL "TOP" CON BOTÓN INTEGRADO ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Source+Sans+Pro:wght@400;700&display=swap');
    
    /* Imagen de fondo */
    .stApp {{
        background-image: url("https://i.postimg.cc/Dfs82Dv6/Gemini_Generated_Image_d7nq1bd7nq1bd7nq.png");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Contenedor de lectura */
    .block-container {{
        background: rgba(255, 255, 255, 0.94);
        padding: 2.5rem;
        border-radius: 25px;
        margin-top: 1.5rem;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.1);
    }}

    /* Título principal (Estética compacta sin espacios) */
    .main-title {{
        font-family: 'Playfair Display', serif;
        color: #00264d;
        font-size: 45px;
        font-weight: 800;
        line-height: 0.82; 
        margin: 0;
        padding: 0;
    }}

    .subtitle-box {{
        display: inline-block;
        border-top: 2px solid #00264d;
        border-bottom: 2px solid #00264d;
        margin-top: 12px;
        padding: 5px 18px;
    }}

    .subtitle-text {{
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 14px;
        letter-spacing: 5px;
        color: #b08d57;
        font-weight: bold;
        margin: 0;
    }}

    /* Pie de página y Botón Contacto Llamativo */
    .footer-container {{
        text-align: center;
        margin-top: 60px;
        padding: 20px;
    }}

    .localmind-text {{
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 13px;
        color: #888;
        letter-spacing: 1px;
        margin-bottom: 15px;
    }}

    .contact-button {{
        display: inline-block;
        padding: 14px 28px;
        background-color: transparent;
        color: #00264d;
        border: 2px solid #b08d57;
        border-radius: 50px;
        text-decoration: none;
        font-family: 'Source Sans Pro', sans-serif;
        font-weight: bold;
        font-size: 15px;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0px 4px 15px rgba(176, 141, 87, 0.2);
    }}

    .contact-button:hover {{
        background-color: #b08d57;
        color: white;
        box-shadow: 0px 6px 20px rgba(176, 141, 87, 0.4);
        transform: translateY(-2px);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
col_head1, col_head2 = st.columns([0.7, 0.3])

with col_head1:
    st.markdown("""
        <div class="main-title">
            La Barca<br>de San<br>Andrés
        </div>
        <div class="subtitle-box">
            <p class="subtitle-text">DESDE 1980</p>
        </div>
        """, unsafe_allow_html=True)

with col_head2:
    st.image("https://i.postimg.cc/dQdLqXs4/Gemini_Generated_Image_kywrxfkywrxfkywr.png", width=120)

st.markdown("<br>", unsafe_allow_html=True)

# --- MENÚ COMPLETO (BASE DE DATOS JSON) ---
# Mantenemos el JSON completo para que la IA tenga toda la información
menu_json = {
    "entrantes": [
        {"plato": "Papas arrugadas con mojo canario", "precio": 5.50, "maridaje": "Yaiza Seco"},
        {"plato": "Gofio escaldado con cebolla roja", "precio": 5.80, "maridaje": "Mencey Chasna Seco"},
        {"plato": "Pulpo a la carmela", "precio": 20.50, "maridaje": "Martinon Blanc de Noir"},
        {"plato": "Queso herreño a la plancha", "precio": 10.50, "maridaje": "Mencey Chasna Afrutado"},
        {"plato": "Lapas a la carmela", "precio": 10.50, "maridaje": "Yaiza Seco"}
    ],
    "carnes": [
        {"plato": "Chuleton de vaca rubia gallega", "precio": 55.00, "unidad": "kg", "maridaje": "Pago de Carraovejas"},
        {"plato": "Solomillo al grill", "precio": 22.90, "maridaje": "Ramon Bilbao Crianza"}
    ],
    "pescados_mariscos": [
        {"plato": "Bogavante a la plancha", "precio": 95.00, "unidad": "kg", "maridaje": "Veuve Clicquot"},
        {"plato": "Pescado fresco del pais", "precio": 38.00, "unidad": "kg", "maridaje": "Martinon Seco"}
    ]
}

# --- PROMPT DEL SISTEMA ---
prompt_sistema = f"""
Actúa como el sumiller experto de 'La Barca de San Andrés'. 
Consulta este menú para responder: {menu_json}
REGLAS:
1. Responde en el idioma del cliente de forma fluida.
2. Cada plato debe incluir su PRECIO y su MARIDAJE recomendado.
3. Sé directo, elegante y profesional.
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
        # Ejemplo de respuesta estructural
        respuesta = "Para acompañar su velada, le recomiendo el **Chuletón de vaca rubia gallega (55,00€/kg)**. Nuestro sumiller sugiere maridarlo con un **Pago de Carraovejas**, un tinto excepcional que potencia la intensidad de la carne."
        st.markdown(respuesta)
        st.session_state.messages.append({"role": "assistant", "content": respuesta})

# --- PIE DE PÁGINA (ESTÉTICA LOCALMIND) ---
st.markdown(f"""
    <div class="footer-container">
        <div class="localmind-text">POWERED BY <b>LOCALMIND.</b></div>
        <a href="https://wa.me/TU_NUMERO_AQUI" target="_blank" class="contact-button">
            ¿Quieres este asistente? Contacta con nosotros
        </a>
    </div>
    """, unsafe_allow_html=True)
