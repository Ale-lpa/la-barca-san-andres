import streamlit as st

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="La Barca de San Andrés", layout="wide")

# --- ESTÉTICA "TOP" (CSS PARA ELIMINAR ESPACIOS Y FIJAR ESTILO) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&display=swap');
    
    /* Título principal con interlineado corregido */
    .main-title {
        font-family: 'Playfair Display', serif;
        color: #00264d;
        font-size: 42px;
        font-weight: 800;
        line-height: 0.85; /* Elimina el espacio entre líneas */
        margin: 0;
        padding: 0;
    }

    /* Subtítulo DESDE 1980 con líneas superior e inferior */
    .subtitle-box {
        display: inline-block;
        border-top: 2px solid #00264d;
        border-bottom: 2px solid #00264d;
        margin-top: 10px;
        padding: 4px 15px;
    }

    .subtitle-text {
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 14px;
        letter-spacing: 4px;
        color: #b08d57;
        font-weight: bold;
        margin: 0;
    }

    /* Contenedor del logo */
    .logo-img {
        display: block;
        margin-left: auto;
        margin-right: 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ESTRUCTURADO ---
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
    # Usando el link del timón dorado
    st.image("https://i.ibb.co/vzYV7mK/timon.png", width=110)

st.markdown("<br>", unsafe_allow_html=True)

# --- EL MENÚ COMPLETO (BASE DE DATOS JSON PARA LA IA) ---
# Aquí está TODO el menú para que la IA no resuma nada
menu_json = {
    "entrantes": [
        {"plato": "Papas arrugadas con mojo canario", "precio": 5.50, "maridaje": "Yaiza Seco"},
        {"plato": "Gofio escaldado con cebolla roja", "precio": 5.80, "maridaje": "Mencey Chasna Seco"},
        {"plato": "Gambas al ajillo", "precio": 12.50, "maridaje": "Jose Pariente"},
        {"plato": "Sardinillas fritas o a la plancha", "precio": 11.20, "maridaje": "Viore Lias"},
        {"plato": "Salteado de verduras con miel y mostaza", "precio": 12.80, "maridaje": "Mencey Chasna Afrutado"},
        {"plato": "Pulpo frito con mojo verde", "precio": 18.80, "maridaje": "Yaiza Seco"},
        {"plato": "Pulpo a la carmela", "precio": 20.50, "maridaje": "Martinon Blanc de Noir"},
        {"plato": "Pulpo a la canaria", "precio": 22.50, "maridaje": "Martinon Blanc de Noir"},
        {"plato": "Queso herreño a la plancha con compota", "precio": 10.50, "maridaje": "Mencey Chasna Afrutado"},
        {"plato": "Queso frito con mermelada de arándanos", "precio": 9.10, "maridaje": "Vivanco Semidulce"},
        {"plato": "Pochas con almejas o langostinos", "precio": 24.50, "maridaje": "Ramon do Casar"}
    ],
    "carnes": [
        {"plato": "Solomillo al grill", "precio": 22.90, "maridaje": "Ramon Bilbao Crianza"},
        {"plato": "Chuleton de vaca rubia gallega", "precio": 55.00, "unidad": "kg", "maridaje": "Pago de Carraovejas"},
        {"plato": "Vueltas de entrecot al jerez", "precio": 16.60, "maridaje": "Figuero 4 meses"},
        {"plato": "Escalope de solomillo", "precio": 20.50, "maridaje": "Azpilicueta Crianza"}
    ],
    "pescados_y_mariscos": [
        {"plato": "Pescado fresco del pais", "precio": 38.00, "unidad": "kg", "maridaje": "Martinon Seco"},
        {"plato": "Bogavante a la plancha", "precio": 95.00, "unidad": "kg", "maridaje": "Veuve Clicquot"},
        {"plato": "Lapas a la carmela con mojo verde", "precio": 10.50, "maridaje": "Yaiza Seco"},
        {"plato": "Almejas salteadas con ajo y perejil", "precio": 19.90, "maridaje": "Gran Bazán Ámbar"},
        {"plato": "Calamares saharianos fritos", "precio": 18.20, "maridaje": "Viña Perez (Verdejo)"}
    ],
    "arroces": [
        {"plato": "Paella de marisco", "precio": 42.80, "maridaje": "Tombu Rosado"},
        {"plato": "Arroz caldoso de bogavante", "precio": 64.00, "maridaje": "Jose Pariente Barrica"}
    ],
    "postres": [
        {"plato": "Mus de gofio", "precio": 5.50, "maridaje": "Yaiza Afrutado"},
        {"plato": "Polvito uruguayo", "precio": 5.50, "maridaje": "Yaiza Afrutado"}
    ]
}

# --- INSTRUCCIONES PARA LA IA ---
# Se le ordena consultar el JSON para cada respuesta
prompt_sistema = f"""
Actúa como el experto sumiller de 'La Barca de San Andrés'.
Consulta SIEMPRE este JSON para tus respuestas: {menu_json}

REGLAS DE ORO:
1. Responde en el idioma en que te hablen (Español, Inglés, etc.).
2. Nunca resumas el menú. Si preguntan por una categoría, dala completa.
3. Por cada plato mencionado, indica su PRECIO y recomienda el MARIDAJE asignado.
4. Tono profesional, directo y sin introducciones innecesarias.
"""

# --- CHAT INTERFAZ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de usuario
if input_usuario := st.chat_input("Hable con el capitán..."):
    st.session_state.messages.append({"role": "user", "content": input_usuario})
    with st.chat_message("user"):
        st.markdown(input_usuario)

    with st.chat_message("assistant"):
        # Simulación de respuesta IA (aquí conectarías tu modelo pasando 'prompt_sistema')
        respuesta = "Nuestro sumiller le recomienda el **Pulpo a la Carmela (20,50€)** maridado con un **Martinón Blanc de Noir**, que resalta su sabor único."
        st.markdown(respuesta)
        st.session_state.messages.append({"role": "assistant", "content": respuesta})
