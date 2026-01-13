import streamlit as st

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="La Barca de San Andrés", layout="wide")

# --- ESTÉTICA REFINADA Y SUTIL (CSS) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Source+Sans+Pro:wght@300;400;700&display=swap');
    
    /* Imagen de fondo */
    .stApp {{
        background-image: url("https://i.postimg.cc/Dfs82Dv6/Gemini_Generated_Image_d7nq1bd7nq1bd7nq.png");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Contenedor principal ultra-limpio */
    .block-container {{
        background: rgba(255, 255, 255, 0.96);
        padding: 3rem;
        border-radius: 30px;
        margin-top: 2rem;
        box-shadow: 0px 15px 35px rgba(0,0,0,0.05);
    }}

    /* Título principal (Estética compacta 0.82) */
    .main-title {{
        font-family: 'Playfair Display', serif;
        color: #00264d;
        font-size: 46px;
        font-weight: 800;
        line-height: 0.82; 
        margin: 0;
        padding: 0;
    }}

    .subtitle-box {{
        display: inline-block;
        border-top: 1px solid #00264d;
        border-bottom: 1px solid #00264d;
        margin-top: 15px;
        padding: 3px 20px;
    }}

    .subtitle-text {{
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 13px;
        letter-spacing: 6px;
        color: #b08d57;
        font-weight: 400;
        margin: 0;
    }}

    /* Pie de página Sutil */
    .footer-container {{
        text-align: center;
        margin-top: 80px;
        padding-bottom: 20px;
    }}

    .localmind-text {{
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 11px;
        color: #aaa;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 15px;
    }}

    .contact-link {{
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 14px;
        color: #b08d57;
        text-decoration: none;
        border-bottom: 1px solid transparent;
        transition: all 0.4s ease;
        padding-bottom: 2px;
        font-weight: 400;
    }}

    .contact-link:hover {{
        color: #00264d;
        border-bottom: 1px solid #00264d;
        letter-spacing: 1px;
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

# --- BASE DE DATOS JSON COMPLETA ---
menu_json = {
    "entrantes": [
        {"plato": "Papas arrugadas con mojo canario", "precio": 5.50, "maridaje": "Yaiza Seco"},
        {"plato": "Gofio escaldado con cebolla roja", "precio": 5.80, "maridaje": "Mencey Chasna Seco"},
        {"plato": "Pulpo a la carmela", "precio": 20.50, "maridaje": "Martinon Blanc de Noir"},
        {"plato": "Lapas a la carmela", "precio": 10.50, "maridaje": "Yaiza Seco"},
        {"plato": "Queso frito con mermelada", "precio": 9.10, "maridaje": "Vivanco Semidulce"}
    ],
    "carnes": [
        {"plato": "Chuleton de vaca rubia gallega", "precio": 55.00, "unidad": "kg", "maridaje": "Pago de Carraovejas"},
        {"plato": "Solomillo al grill", "precio": 22.90, "maridaje": "Ramón Bilbao Crianza"}
    ],
    "pescados_mariscos": [
        {"plato": "Bogavante a la plancha", "precio": 95.00, "unidad": "kg", "maridaje": "Veuve Clicquot"},
        {"plato": "Arroz caldoso de bogavante", "precio": 64.00, "maridaje": "Jose Pariente Barrica"}
    ]
}

# --- LÓGICA DE IA ---
# (Aquí se conecta con el motor de IA usando el prompt_sistema definido antes)

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
    
    # Respuesta simulada basada en el menú
    with st.chat_message("assistant"):
        respuesta = "Le recomiendo nuestro **Pulpo a la Carmela (20,50€)**. Su maridaje ideal es el **Martinon Blanc de Noir**, que aporta la estructura perfecta para este plato."
        st.markdown(respuesta)
        st.session_state.messages.append({"role": "assistant", "content": respuesta})

# --- PIE DE PÁGINA SUTIL (CON TU NÚMERO) ---
st.markdown(f"""
    <div class="footer-container">
        <div class="localmind-text">POWERED BY <b>LOCALMIND.</b></div>
        <a href="https://wa.me/34602566673" target="_blank" class="contact-link">
            ¿Quieres este asistente? Contacta con nosotros
        </a>
    </div>
    """, unsafe_allow_html=True)
