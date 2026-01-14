import streamlit as st
import openai  # O tu proveedor de IA (puedes ajustar la función de respuesta)

# 1. CONFIGURACIÓN DE PÁGINA Y ESTÉTICA (CSS)
st.set_page_config(page_title="La Barca de San Andrés", page_icon="⚓")

# CSS personalizado para arreglar el nombre y el diseño
st.markdown("""
    <style>
    .restaurant-title {
        color: #002147;
        font-family: 'Serif';
        font-size: 42px;
        font-weight: bold;
        line-height: 1.1;
        margin-bottom: 0px;
    }
    .restaurant-subtitle {
        color: #C5A059;
        letter-spacing: 5px;
        font-size: 14px;
        margin-top: -10px;
        border-top: 1px solid #002147;
        display: inline-block;
        padding-top: 5px;
    }
    .footer {
        position: fixed;
        bottom: 10px;
        width: 100%;
        text-align: center;
        font-size: 12px;
        color: #666;
    }
    </style>
""", unsafe_allow_html=True)

# 2. CABECERA (ESTÉTICA CORREGIDA)
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown('<p class="restaurant-title">La Barca de<br>San Andrés</p>', unsafe_allow_html=True)
    st.markdown('<p class="restaurant-subtitle">DESDE 1980</p>', unsafe_allow_html=True)
with col2:
    # Asegúrate de tener el logo en la ruta correcta o usar una URL
    st.image("https://raw.githubusercontent.com/tu-usuario/tu-repo/main/logo_timon.png", width=100) 

# 3. SYSTEM PROMPT (EL CEREBRO)
SYSTEM_PROMPT = """
Eres el sumiller virtual de 'La Barca de San Andrés'. 
REGLAS CRÍTICAS:
1. IDIOMA: Responde SIEMPRE en el idioma que te hable el cliente (Detección automática por mensaje).
2. NO REPETICIÓN: Lee el historial. Si el cliente ya recibió una recomendación, no la repitas. Avanza en la conversación.
3. PRECIO Y MARIDAJE: Cada plato mencionado debe ir con su precio y su vino sugerido.
   - Ejemplo: 'Papas arrugadas (5,50€). Sugerimos Yaiza Seco.'

MENÚ Y MARIDAJES:
- Entrantes: Papas arrugadas (5,50€ - Yaiza Seco), Gofio (5,80€ - Mencey Chasna), Pulpo Carmela (20,50€ - Martinón Blanc de Noir).
- Carnes: Solomillo (22,90€ - Ramón Bilbao), Chuletón (55€/kg - Pago de Carraovejas).
- Pescados: Pescado fresco (38€/kg - Martinón Seco), Lapas (10,50€ - Yaiza Seco).
- Arroces: Arroz Bogavante (64€ - Jose Pariente Barrica).
- Postres: Mus de Gofio (5,50€ - Yaiza Afrutado).
(Añade aquí el resto de la carta que compartimos anteriormente).
"""

# 4. LÓGICA DE MENSAJES E ICONOS
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial con iconos personalizados
for message in st.session_state.messages:
    # Usuario = Pescado, Asistente = Ancla
    avatar = "🐟" if message["role"] == "user" else "⚓"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Entrada de chat
if prompt := st.chat_input("Hable con el capitán..."):
    # Guardar y mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🐟"):
        st.markdown(prompt)

    # Generar respuesta de la IA
    with st.chat_message("assistant", avatar="⚓"):
        # Preparamos el contexto completo para evitar repeticiones
        full_history = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
        
        # Simulación de respuesta (Sustituir por tu llamada real a la API)
        # response = client.chat.completions.create(model="gpt-4", messages=full_history)
        # full_response = response.choices[0].message.content
        full_response = "Esta es una respuesta de prueba que sigue el System Prompt." 
        
        st.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# 5. CONTACTO Y POWERED BY
st.markdown("---")
st.markdown("""
    <div style="text-align: center;">
        <p>POWERED BY</p>
        <h3 style="margin-top: -15px;">Localmind.</h3>
        <p>¿Quieres este asistente? <a href="https://wa.me/tu_numero_aqui" target="_blank">Contacta con nosotros</a></p>
    </div>
""", unsafe_allow_html=True)
