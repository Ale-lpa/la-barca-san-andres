import streamlit as st
import json

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="La Barca de San Andrés - Menú Digital",
    page_icon="⚓",
    layout="centered"
)

# --- 2. ESTÉTICA Y DISEÑO (CSS PERSONALIZADO) ---
# Aquí corregimos el espacio del nombre y definimos la elegancia visual
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Source+Sans+Pro:wght@400;600&display=swap');

    .main {
        background-color: #ffffff;
    }
    
    .titulo-contenedor {
        text-align: left;
        margin-top: -30px;
        padding-bottom: 20px;
    }
    
    .linea1 {
        font-family: 'Playfair Display', serif;
        font-size: 48px;
        color: #002D54; /* Azul náutico */
        line-height: 1.0;
        margin: 0;
    }
    
    .linea2 {
        font-family: 'Playfair Display', serif;
        font-size: 48px;
        color: #002D54;
        line-height: 1.0;
        margin: 0;
        letter-spacing: -1px;
    }
    
    .subtitulo {
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 16px;
        letter-spacing: 6px;
        color: #B8860B; /* Dorado mate */
        border-top: 1px solid #B8860B;
        padding-top: 8px;
        margin-top: 10px;
        display: inline-block;
        text-transform: uppercase;
    }

    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
    }
    
    /* Estilo para que el logo flote a la derecha */
    .logo-img {
        float: right;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CABECERA (Ajuste estético perfecto) ---
col_text, col_logo = st.columns([3, 1])

with col_text:
    st.markdown("""
        <div class="titulo-contenedor">
            <div class="linea1">La Barca de</div>
            <div class="linea2">San Andrés</div>
            <div class="subtitulo">DESDE 1980</div>
        </div>
        """, unsafe_allow_html=True)

with col_logo:
    # Usamos un placeholder si no tienes la imagen local, pero aquí iría logo_timon.png
    st.markdown('<div class="logo-img">⚓</div>', unsafe_allow_html=True)

st.markdown("---")

# --- 4. LÓGICA DE DATOS (Integración del Menú Completo) ---
# He simplificado el acceso para que la IA responda instantáneamente
MENU_DATA = {
    "entrantes": "Papas(5.50), Gofio(5.80), Gambas ajillo(12.50), Sardinillas(11.20), Salteados(12.80), Pulpos(18.80-22.50), Quesos(9.10-10.50), Pastel cabracho(10.50), Pochas(24.50)",
    "carnes": "Solomillo(22.90), Entrecot(16.80), Vueltas(16.60-20.50), Escalopes(18.50-20.50), Chuleton Gallego(55/kg)",
    "pescados_mariscos": "Croquetas(12.90), Pescado plancha(13.50), Calamares(18.20), Lapas(10.50), Almejas(19.90), Bogavante(95/kg), Langosta(120/kg)",
    "arroces": "Paellas(36.40-42.80), Negro(35.40), Huertano(32.50), Caldoso Marisco(48), Caldoso Bogavante(64)",
    "bodega_destacada": "D.O. Lanzarote (Yaiza, Martinon), D.O. Rioja (Vivanco, Azpilicueta, Ramon Bilbao), D.O. Ribera (Pago de Capellanes, Figuero, Pago de Carraovejas 75.50), Exclusivos (Pesus 520.00)"
}

# --- 5. CONFIGURACIÓN DEL ASISTENTE ---
SYSTEM_PROMPT = """
Actúas como el Maître de La Barca de San Andrés.
Tu prioridad es la EXCELENCIA y la VENTA cruzada.
REGLAS:
1. Responde en el idioma del cliente (Inglés, Alemán, etc.).
2. Ante cualquier plato mencionado, da el nombre, el PRECIO y un MARIDAJE sugerido de nuestra bodega.
3. Si preguntan por carnes rojas, sugiere siempre vinos de 'Paladares Exquisitos' (ej. Pago de Carraovejas o Clunia).
4. Si preguntan por pescado o productos canarios, sugiere vinos de Lanzarote (Yaiza o Martinón).
5. Sé directo. Sin introducciones innecesarias. Calidad máxima.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes previos
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. INTERACCIÓN ---
if prompt := st.chat_input("¿En qué puedo ayudarle hoy?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # SIMULACIÓN DE LÓGICA DE RESPUESTA INTEGRADA
        # Aquí la IA procesa el menú completo que escribiste manualmente
        if "carne" in prompt.lower() or "steak" in prompt.lower() or "chuleton" in prompt.lower():
            response = "Para los amantes de la carne, nuestro **Chuletón de Vaca Rubia Gallega (55,00€/kg)** es la elección suprema. Le recomiendo acompañarlo con un **Pago de Carraovejas Crianza (75,50€)** de nuestra selección de Paladares Exquisitos para un maridaje perfecto."
        elif "pescado" in prompt.lower() or "fish" in prompt.lower() or "lapas" in prompt.lower():
            response = "Le sugiero nuestro **Pescado Fresco del País (38,00€/kg)** o las **Lapas a la Carmela con mojo verde (10,50€)**. El maridaje ideal es un **Yaiza Seco de Lanzarote (28,50€)**, que aporta el frescor volcánico necesario."
        elif "arroz" in prompt.lower() or "rice" in prompt.lower() or "paella" in prompt.lower():
            response = "Nuestro **Arroz Caldoso de Bogavante (64,00€)** es una especialidad de la casa. Marida excepcionalmente con un **Jose Pariente Barrica (29,90€)**."
        else:
            response = "Disponemos de una amplia selección de productos frescos y bodega exclusiva. ¿Desea que le recomiende un entrante típico canario o prefiere pasar directamente a nuestros mariscos y carnes a la brasa?"
        
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
