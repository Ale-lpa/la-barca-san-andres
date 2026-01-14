import streamlit as st
import openai

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="La Barca de San Andrés", layout="centered")

# --- 2. ESTÉTICA REFINADA (CSS) ---
# Solución definitiva al espaciado del nombre y estilo de las capturas
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');
    
    .stApp {
        background-image: url("https://i.postimg.cc/Dfs82Dv6/Gemini_Generated_Image_d7nq1bd7nq1bd7nq.png");
        background-size: cover;
        background-attachment: fixed;
    }
    
    .restaurant-title {
        font-family: 'Playfair Display', serif;
        color: #002147;
        font-size: 42px;
        font-weight: 700;
        line-height: 0.9; /* Elimina el espacio excesivo entre líneas */
        margin: 0;
        padding: 0;
    }
    
    .restaurant-subtitle {
        color: #C5A059;
        letter-spacing: 5px;
        font-size: 14px;
        font-weight: bold;
        border-top: 1px solid #002147;
        display: inline-block;
        margin-top: 10px;
        padding-top: 5px;
        text-transform: uppercase;
    }

    /* Ajuste para que el nombre y el logo queden alineados */
    .header-box {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 30px;
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
    st.image("https://i.imgur.com/TK0Uo6I.png", width=110) # Tu imagen del timón

# --- 4. SYSTEM PROMPT (CEREBRO DEL ASISTENTE) ---
SYSTEM_PROMPT = """
Eres el sumiller virtual de 'La Barca de San Andrés'. 

INSTRUCCIONES CRÍTICAS DE RESPUESTA:
1. IDIOMA: Detecta el idioma del cliente. Si preguntan en inglés, responde en inglés. Si es en español, responde en español.
2. NO REPETICIÓN: Revisa el historial de chat. Si ya recomendaste un plato (ej. Pulpo a la Carmela), NO lo repitas. Ofrece una alternativa nueva.
3. MARIDAJE TOTAL: Absolutamente CADA plato que menciones debe ir acompañado de su PRECIO y su VINO sugerido.

BASE DE DATOS DE MARIDAJES:
- Papas arrugadas (5,50€): Yaiza Seco (Malvasía).
- Gofio escaldado (5,80€): Mencey Chasna Seco.
- Gambas al ajillo (12,50€): Jose Pariente (Verdejo).
- Pulpo a la Carmela (20,50€): Martinón Blanc de Noir.
- Pulpo Frito (18,80€): Yaiza Seco.
- Queso Herreño plancha (10,50€): Mencey Chasna Afrutado.
- Chuletón Vaca Rubia (55€/kg): Pago de Carraovejas.
- Solomillo grill (22,90€): Ramón Bilbao Crianza.
- Pescado fresco (38€/kg): Martinón Seco.
- Lapas con mojo (10,50€): Yaiza Seco.
- Bogavante plancha (95€/kg): Veuve Clicquot.
- Arroz Caldoso Bogavante (64€): Jose Pariente Barrica.
- Paella Marisco (42,80€): Tombu Rosado.
- Polvito Uruguayo o Mus de Gofio (5,50€): Yaiza Afrutado.

Si el cliente pide contacto, indica que contacte por WhatsApp y menciona 'Powered by Localmind'.
"""

# --- 5. LÓGICA DE CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial con iconos: Usuario (Pescado) y Asistente (Ancla)
for message in st.session_state.messages:
    icon = "🐟" if message["role"] == "user" else "⚓"
    with st.chat_message(message["role"], avatar=icon):
        st.markdown(message["content"])

if prompt := st.chat_input("Hable con el capitán..."):
    # 1. Guardar mensaje de usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🐟"):
        st.markdown(prompt)

    # 2. Generar respuesta con historial para evitar repeticiones y detectar idioma
    with st.chat_message("assistant", avatar="⚓"):
        # Construimos el contexto completo
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

# --- 6. PIE DE PÁGINA (BRANDING Y CONTACTO) ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center; border-top: 0.5px solid #ccc; padding-top: 20px;">
        <p style="font-size: 12px; color: #666; letter-spacing: 2px;">POWERED BY</p>
        <h3 style="margin-top: -10px; color: #002147; font-family: sans-serif;">Localmind.</h3>
        <p style="font-size: 14px;">¿Quieres este asistente? <a href="https://wa.me/TU_NUMERO_AQUI" style="color: #C5A059; text-decoration: none; font-weight: bold;">Contacta con nosotros</a></p>
    </div>
""", unsafe_allow_html=True)
