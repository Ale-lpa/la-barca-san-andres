import streamlit as st
import json

# ⚓ Configuración
st.set_page_config(page_title="La Barca de San Andrés", page_icon="⚓", layout="centered")

# --- ESTÉTICA (Mantenemos lo que ya te gusta) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Poppins:wght@300;400;500&display=swap');
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.95), rgba(0,0,0,0.95)), 
                    url('https://images.unsplash.com/photo-1550966841-391ad29a01d5?q=80&w=2070&auto=format&fit=crop'); 
        background-size: cover; background-attachment: fixed;
    }
    #MainMenu, footer, header {visibility: hidden;}
    .header-box { text-align: center; padding: 20px 10px 5px 10px; border-bottom: 2px solid #D4AF37; margin-bottom: 10px; }
    .header-box h1 { font-family: 'Playfair Display', serif; color: #D4AF37; font-size: 2rem; letter-spacing: 4px; margin: 0; text-transform: uppercase; }
    .header-box p { font-family: 'Poppins', sans-serif; color: #D4AF37; font-size: 0.8rem; letter-spacing: 3px; margin: 0; opacity: 0.9; }
    .chat-container { display: flex; flex-direction: column; gap: 15px; padding-bottom: 150px !important; }
    .bubble-assistant { background: rgba(0, 35, 102, 0.7); border-left: 5px solid #D4AF37; padding: 15px; border-radius: 5px 20px 20px 20px; color: #F9F7F2; font-family: 'Poppins', sans-serif; max-width: 85%; align-self: flex-start; }
    .bubble-user { background: rgba(212, 175, 55, 0.15); border-right: 5px solid #D4AF37; padding: 12px; border-radius: 20px 5px 20px 20px; color: #D4AF37; text-align: right; font-family: 'Poppins', sans-serif; max-width: 80%; align-self: flex-end; }
    .label-captain { color: #D4AF37; font-weight: 700; font-size: 0.7rem; margin-bottom: 5px; display: block; }
    div[data-testid="stChatInput"] { padding-bottom: 20px !important; }
    </style>
    <div class="header-box">
        <h1>⚓ LA BARCA DE SAN ANDRÉS ⚓</h1>
        <p>DESDE 1980</p>
    </div>
    """, unsafe_allow_html=True)

# --- MOTOR DE INTELIGENCIA Y VENTAS ---
def get_captain_response(user_input, menu_data):
    input_lower = user_input.lower()
    
    # 🌍 Lógica Multilingüe Básica (Detecta idiomas comunes)
    is_english = any(word in input_lower for word in ["fish", "wine", "hello", "menu", "price"])
    is_german = any(word in input_lower for word in ["fisch", "wein", "hallo", "karte"])

    # 1. Búsqueda de Pescado
    if any(word in input_lower for word in ["pescado", "fish", "fisch", "fresco"]):
        resp = f"Nuestro género es del día. Tenemos {menu_data['menu']['platos_principales'][0]['plato']} a {menu_data['menu']['platos_principales'][0]['precio']}."
        upsell = f" ¿Le gustaría maridarlo con un vino {menu_data['menu']['bodega'][0]['nombre']}? Es la combinación perfecta."
        return resp + upsell if not is_english else "We have fresh local fish today. I recommend the Cherne or Abadejo. Would you like a glass of Yaiza white wine with that?"

    # 2. Búsqueda de Arroces (Venta Alta)
    if "arroz" in input_lower or "rice" in input_lower or "bogavante" in input_lower:
        item = menu_data['menu']['platos_principales'][2]
        return f"¡Ah, el {item['plato']}! Es nuestra gran especialidad ({item['precio']}). Lo preparamos al momento para mínimo 2 personas. ¿Desea que le reservemos una mesa para disfrutarlo?"

    # 3. Búsqueda de Vinos
    if "vino" in input_lower or "wine" in input_lower or "beber" in input_lower:
        vinos = ", ".join([v['nombre'] for v in menu_data['menu']['bodega'][:2]])
        return f"En nuestra bodega destacan el {vinos}. ¿Prefiere un blanco de Lanzarote o algo de nuestra tierra en Gran Canaria?"

    # 4. Respuesta por defecto con Venta Sugerida
    if is_english:
        return "Welcome! I suggest our fresh limpets (Lapas) to start, and then our famous lobster rice. What would you like to see first?"
    
    return "Como Capitán, le sugiero empezar con unas Lapas a la Carmela y seguir con el pescado fresco. ¿Le apetece ver los precios de los entrantes?"

# --- FLUJO DEL CHAT ---
try:
    with open('knowledge.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except:
    st.error("Error cargando la carta.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "¡Bienvenidos a bordo de La Barca de San Andrés! 🌊 Es un placer recibirles. Hoy el mar nos ha traído un género espectacular; ¿les gustaría probar nuestra recomendación del pescado del día?"}]

st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for m in st.session_state.messages:
    cls = "bubble-assistant" if m["role"] == "assistant" else "bubble-user"
    lbl = '<span class="label-captain">⚓ EL CAPITÁN</span>' if m["role"] == "assistant" else ""
    st.markdown(f'<div class="{cls}">{lbl}{m["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if prompt := st.chat_input("Hable con el Capitán..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Generar respuesta inteligente
    answer = get_captain_response(prompt, data)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()
