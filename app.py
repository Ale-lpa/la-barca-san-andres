import streamlit as st
import openai

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="La Barca de San Andrés", layout="centered")

# --- 2. ESTÉTICA REFINADA (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');
    
    /* Fondo fijo */
    .stApp {
        background-image: url("https://i.postimg.cc/Dfs82Dv6/Gemini_Generated_Image_d7nq1bd7nq1bd7nq.png");
        background-size: cover;
        background-attachment: fixed;
        background-position: center center;
    }
    
    /* ELIMINAR MÁRGENES SUPERIORES PARA PEGAR AL BORDE */
    .block-container {
        padding-top: 1rem !important;
    }

    /* 1. LOGO PEGADO A LA ESQUINA IZQUIERDA */
    .logo-corner {
        margin-top: -10px;
        margin-left: -20px;
    }

    /* ESTILO DEL NOMBRE (A la derecha) */
    .restaurant-title {
        font-family: 'Playfair Display', serif;
        color: #002147;
        font-size: 65px; 
        font-weight: 700;
        line-height: 0.85; 
        margin: 0;
        padding: 0;
        text-align: right;
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
        float: right;
    }

    /* FOOTER (CONTACTO) */
    .brand-line {
        color: #002147 !important;
        font-family: sans-serif;
        font-weight: 800;
        font-size: 18px;
        letter-spacing: 1px;
        margin: 0;
        padding: 0;
        text-transform: lowercase;
    }

    /* FOOTER FIJO AL FONDO */
    .sticky-footer-container {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        text-align: center;
        padding-top: 15px;
        padding-bottom: 70px; 
        background: linear-gradient(to top, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0) 100%);
        z-index: 0;
    }
    
    .main .block-container {
        padding-bottom: 220px; 
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. CABECERA (LOGO ESQUINA IZQ | NOMBRE DERECHA) ---
col_logo, col_text = st.columns([1, 3])
with col_logo:
    # Logo pegado a la esquina
    st.markdown('<div class="logo-corner">', unsafe_allow_html=True)
    st.image("https://i.imgur.com/FIn4ep3.png", width=95) 
    st.markdown('</div>', unsafe_allow_html=True)

with col_text:
    st.markdown("""
        <div style="width: 100%;">
            <p class="restaurant-title">La Barca de<br>San Andrés</p>
            <p class="restaurant-subtitle">desde 1980</p>
        </div>
    """, unsafe_allow_html=True)

# --- 4. SYSTEM PROMPT ---
SYSTEM_PROMPT = """
Eres el sumiller virtual de 'La Barca de San Andrés'. 
INSTRUCCIONES:
1. IDIOMA: Responde en el idioma del cliente.
2. NO REPETICIÓN: No repitas recomendaciones.
3. MARIDAJE TOTAL: CADA plato debe ir con su PRECIO y VINO sugerido.

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
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model="gpt-4",
            messages=contexto_chat,
            temperature=0.7
        )
        full_response = response.choices[0].message.content
        st.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- 6. PIE DE PÁGINA (BRANDING Y CONTACTO SOLICITADO) ---
st.markdown(f"""
    <div class="sticky-footer-container">
        <p class="brand-line">powered by localmind.</p>
        <p style="margin-top: 5px;">
            <a href="https://wa.me/TU_NUMERO_AQUI" target="_blank" style="color: #C5A059; text-decoration: none; font-weight: bold; font-size: 15px;">
                ¿Quieres este asistente?
            </a>
        </p>
    </div>
""", unsafe_allow_html=True)
