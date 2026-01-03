import streamlit as st
import json

# Configuración visual de la App
st.set_page_config(page_title="La Barca de San Andrés - Asistente", page_icon="⚓")

# CSS personalizado para estilo Luxury Nautical
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Poppins:wght@300;400&display=swap');
    
    .stApp { background-color: #F9F7F2; }
    
    .header-container {
        background-color: #002366; /* Azul Marino */
        color: white;
        padding: 30px;
        text-align: center;
        border-bottom: 5px solid #C5A059; /* Dorado */
        border-radius: 0 0 20px 20px;
        margin-bottom: 20px;
        font-family: 'Playfair Display', serif;
    }
    
    .header-container h1 { letter-spacing: 4px; font-size: 2.2rem; margin: 0; }
    .header-container p { font-size: 0.9rem; letter-spacing: 5px; opacity: 0.8; margin-top: 5px; }
    
    .stChatMessage { border-radius: 15px; border: 1px solid #E5E1D8; }
    
    .branding-footer {
        text-align: center;
        font-size: 0.75rem;
        color: #888;
        padding: 20px;
    }
    .branding-footer b { color: #C5A059; }
    </style>
    
    <div class="header-container">
        <h1>LA BARCA</h1>
        <p>SAN ANDRÉS</p>
    </div>
    """, unsafe_allow_html=True)

# Cargar el cerebro
with open('knowledge.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Inicializar chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": f"⚓ ¡Bienvenidos a bordo! Soy el Capitán de La Barca. ¿Desean probar nuestra sugerencia de hoy: {data['sugerencia_dia']}? O quizás prefieran que les explique nuestro pescado fresco del día."}
    ]

# Renderizar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Lógica de respuesta (Multilingüe y técnica)
if prompt := st.chat_input("Escriba su pregunta aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Aquí conectarías con tu modelo de IA. Para la demo, el bot usa el conocimiento real:
        response = f"Como Capitán de La Barca, le recomiendo nuestro género estrella: {data['menu']['platos_principales'][2]['plato']} ({data['menu']['platos_principales'][2]['precio']}). Para maridar, un {data['menu']['bodega'][0]['nombre']} es la elección de los expertos. ¿Desea ver los precios de nuestros pescados frescos?"
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

st.markdown("<div class='branding-footer'>Diseñado por <b>LocalMind AI</b> • Alejandro Moreno</div>", unsafe_allow_html=True)
