import streamlit as st
import openai

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="La Barca de San Andrés", layout="centered")

# --- 2. ESTÉTICA REFINADA (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');
    
    .stApp {
        background-image: url("https://i.postimg.cc/Dfs82Dv6/Gemini_Generated_Image_d7nq1bd7nq1bd7nq.png");
        background-size: cover;
        background-attachment: fixed;
    }
    
    /* 3. NOMBRE DEL LOCAL MÁS GRANDE */
    .restaurant-title {
        font-family: 'Playfair Display', serif;
        color: #002147;
        font-size: 55px; /* Aumentado de 42px a 55px */
        font-weight: 700;
        line-height: 0.85; 
        margin: 0;
        padding: 0;
    }
    
    .restaurant-subtitle {
        color: #C5A059;
        letter-spacing: 5px;
        font-size: 16px;
        font-weight: bold;
        border-top: 1px solid #002147;
        display: inline-block;
        margin-top: 10px;
        padding-top: 5px;
        text-transform: uppercase;
    }

    /* 2. COLOR "POWERED BY" EN AZUL CORPORATIVO */
    .powered-by-text {
        font-size: 12px; 
        color: #002147; /* Mismo azul que Localmind */
        letter-spacing: 2px;
        font-weight: bold;
    }
    
    .brand-name {
        margin-top: -10px; 
        color: #002147; 
        font-family: sans-serif;
        font-weight: 800;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. CABECERA ---
col_text, col_logo = st.columns([3, 1])
with col_text:
    st.markdown("""
        <div>
            <p class="restaurant-title">La Barca de<br>San Andrés</p>
            <p class="restaurant-subtitle">desde 1980</p>
        </div>
    """, unsafe_allow_html=True)
with col_logo:
    # 1. NUEVO LOGO ACTUALIZADO
    st.image("https://i.imgur.com/FIn4ep3.png", width=130) 

# --- 4. SYSTEM PROMPT (CEREBRO DEL ASISTENTE) ---
SYSTEM_PROMPT = """
Eres el sumiller virtual de 'La Barca de San Andrés'. 

INSTRUCCIONES CRÍTICAS:
1. IDIOMA: Responde siempre en el idioma del cliente.
2. NO REPETICIÓN: Si ya recomendaste un plato, ofrece uno nuevo.
3. MARIDAJE TOTAL: CADA plato debe ir con su PRECIO y su VINO sugerido.

MENÚ Y MARIDAJES:
- Papas arrugadas (5,50€): Yaiza Seco.
- Gofio escaldado (5,80€): Mencey Chasna Seco.
- Gambas al ajillo (12,50€): Jose Pariente.
- Pulpo a la Carmela (20,50€): Martinón Blanc de Noir.
- Chuletón Vaca Rubia (55€/kg): Pago de Carraovejas.
- Pescado fresco (38€/kg): Martinón Seco.
- Lapas con mojo (10,50€): Yaiza Seco.
- Arroz Caldoso Bogavante (64€): Jose Pariente Barrica.
- Polvito Uruguayo (5,50€): Yaiza Afrutado.

Contacto: WhatsApp. Asistente: 'Powered by Localmind'.
"""

# --- 5. LÓGICA DE CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Iconos: Usuario (Pescado 🐟) y Asistente (Ancla ⚓)
for message in st.session_state.messages:
    icon = "🐟" if message["role"] == "user" else "⚓"
    with st.chat_message(message["role"], avatar=icon):
        st.markdown(message["content"])

if prompt := st.chat_input("Hable con el capitán..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🐟"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="⚓"):
        contexto_chat = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
        
        # Llamada a la API (Sustituir con tu clave)
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model="gpt-4",
            messages=contexto_chat,
            temperature=0.7
        )
        full_response = response.choices[0].message.content
        st.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- 6. PIE DE PÁGINA (BRANDING UNIFICADO) ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center; border-top: 0.5px solid #002147; padding-top: 20px;">
        <p class="powered-by-text">POWERED BY</p>
        <h2 class="brand-name">Localmind.</h2>
        <p style="font-size: 14px;">¿Quieres este asistente? <a href="https://wa.me/TU_NUMERO_AQUI" style="color: #C5A059; text-decoration: none; font-weight: bold;">Contacta con nosotros</a></p>
    </div>
""", unsafe_allow_html=True)
