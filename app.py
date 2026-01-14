import streamlit as st
import openai  # Asegúrate de tener instalada la librería: pip install openai

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="La Barca de San Andrés", layout="centered")

# --- 2. ESTÉTICA REFINADA (CSS) ---
# He ajustado el CSS para que el nombre se vea compacto y elegante como en la captura 33553
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');
    
    .stApp {
        background-image: url("https://i.postimg.cc/Dfs82Dv6/Gemini_Generated_Image_d7nq1bd7nq1bd7nq.png");
        background-size: cover;
        background-attachment: fixed;
    }
    
    .header-container {
        text-align: left;
        margin-bottom: 20px;
    }
    
    .restaurant-title {
        font-family: 'Playfair Display', serif;
        color: #002147;
        font-size: 45px;
        font-weight: 700;
        line-height: 1.0; /* Arregla el espacio entre líneas */
        margin: 0;
    }
    
    .restaurant-subtitle {
        color: #C5A059;
        letter-spacing: 4px;
        font-size: 16px;
        font-weight: bold;
        border-top: 2px solid #002147;
        display: inline-block;
        margin-top: 5px;
        padding-top: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. CABECERA ---
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("""
        <div class="header-container">
            <p class="restaurant-title">La Barca de<br>San Andrés</p>
            <p class="restaurant-subtitle">DESDE 1980</p>
        </div>
    """, unsafe_allow_html=True)
with col2:
    # Usando el logo del timón dorado
    st.image("https://i.postimg.cc/k4m6fN9Z/logo-barca.png", width=110)

# --- 4. SYSTEM PROMPT (CEREBRO) ---
# Aquí está toda la lógica de maridaje y comportamiento
SYSTEM_PROMPT = """
Eres el sumiller y capitán virtual de 'La Barca de San Andrés'. 
REGLAS ABSOLUTAS:
1. IDIOMA: Responde SIEMPRE en el mismo idioma que te hable el cliente.
2. NO REPETICIÓN: Si ya recomendaste algo, no lo vuelvas a decir. Ofrece alternativas.
3. MARIDAJE Y PRECIO: Por cada plato, indica PRECIO y VINO sugerido.
4. TONO: Profesional, acogedor y experto.

MENÚ Y MARIDAJES CLAVE:
- Papas arrugadas (5,50€) -> Yaiza Seco.
- Gofio escaldado (5,80€) -> Mencey Chasna Seco.
- Pulpo a la Carmela (20,50€) -> Martinón Blanc de Noir.
- Chuletón Vaca Rubia (55€/kg) -> Pago de Carraovejas.
- Pescado Fresco (38€/kg) -> Martinón Seco.
- Arroz Caldoso Bogavante (64€) -> Jose Pariente Barrica.
- Polvito Uruguayo (5,50€) -> Yaiza Afrutado.

Si el cliente pregunta por contacto, di que contacte por WhatsApp y que este asistente es 'Powered by Localmind'.
"""

# --- 5. LÓGICA DEL CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostramos historial con los iconos solicitados: Pescado (Usuario) y Ancla (Bot)
for message in st.session_state.messages:
    avatar_icon = "🐟" if message["role"] == "user" else "⚓"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

# Entrada de usuario
if prompt := st.chat_input("Hable con el capitán..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🐟"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="⚓"):
        # Se envía el SYSTEM_PROMPT + Historial completo para que no se repita y sepa el idioma
        contexto = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
        
        # --- LLAMADA A LA API ---
        # Sustituye 'tu_api_key' por tu clave real o usa st.secrets["OPENAI_API_KEY"]
        client = openai.OpenAI(api_key="TU_CLAVE_AQUI")
        response = client.chat.completions.create(
            model="gpt-4", # o gpt-3.5-turbo
            messages=contexto
        )
        full_response = response.choices[0].message.content
        st.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- 6. PIE DE PÁGINA Y CONTACTO ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center; border-top: 1px solid #ddd; padding-top: 20px;">
        <p style="color: #666; font-size: 14px;">POWERED BY</p>
        <h2 style="margin-top: -10px; color: #002147;">Localmind.</h2>
        <p>¿Quieres este asistente? <a href="https://wa.me/TU_NUMERO_AQUI" style="color: #C5A059; text-decoration: none; font-weight: bold;">Contacta con nosotros</a></p>
    </div>
""", unsafe_allow_html=True)
