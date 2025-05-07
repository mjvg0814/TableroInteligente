import os
import streamlit as st
import base64
from openai import OpenAI
import openai
from PIL import Image
import numpy as np
from streamlit_drawable_canvas import st_canvas

# 💖 Función para codificar la imagen
def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            return encoded_image
    except FileNotFoundError:
        return "Error no dibujaste bien"

# 🎨 Configuración de la página
st.set_page_config(page_title='Panel de Control Encantado', page_icon="")
st.title('Bienvenida, pequeña artista digital!')

# 🧁 Sidebar adorable
with st.sidebar:
    st.header("Ajustes rápidos")
    st.write("Dibuja con libertad: ¡La IA transformará tus trazos en arte inteligente!")
    st.markdown("---")
    st.subheader("Pincel")
    stroke_width = st.slider('Espesor del trazo ', 1, 30, 5)
    stroke_color = st.color_picker("Color del fondo", "#000000")
    bg_base_color = st.color_picker("Color del fondo", "#FFFFFF")
    bg_opacity = st.slider("Transparencia del fondo 🌫️", 0.0, 1.0, 1.0, 0.05)

# 🌟 Convertir HEX a RGBA
def hex_to_rgba(hex_color, alpha):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"

bg_color = hex_to_rgba(bg_base_color, bg_opacity)

# 🖼️ Área de dibujo
st.subheader("Dibuja tu idea más épica y deja que la IA la interprete con poder")
canvas_result = st_canvas(
    fill_color="rgba(255, 182, 193, 0.4)",  # rosado pastel con transparencia
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=300,
    width=400,
    drawing_mode="freedraw",
    key="canvas_cute"
)

# 🔐 Ingreso de clave API
ke = st.text_input('Clave de Hechizo (API Key)', type='password')
os.environ['OPENAI_API_KEY'] = ke
api_key = os.environ.get('OPENAI_API_KEY')

# 🧠 Botón para analizar
analyze_button = st.button("Reconoce", type="primary")

if canvas_result.image_data is not None and api_key and analyze_button:
    with st.spinner("Descifrando los secretos de tu creatividad... (¡sorpresas en camino!)"):
        input_numpy_array = np.array(canvas_result.image_data)
        input_image = Image.fromarray(input_numpy_array.astype('uint8'),'RGBA')
        input_image.save('img.png')

        base64_image = encode_image_to_base64("img.png")
        prompt_text = "Explica brevemente la imagen en español"

        try:
            message_placeholder = st.empty()
            response = openai.chat.completions.create(
              model="gpt-4o-mini",
              messages=[
                {
                  "role": "user",
                  "content": [
                    {"type": "text", "text": prompt_text},
                    {
                      "type": "image_url",
                      "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                    },
                  ],
                }
              ],
              max_tokens=500,
            )

            full_response = response.choices[0].message.content
            message_placeholder.markdown("Respuesta encantada del algoritmo:*\n\n" + full_response)

        except Exception as e:
            st.error(f"🚨 ¡Algo salió mal!: {e}")
else:
    if not api_key:
        st.warning("🔐 Por favor ingresa tu clave mágica (API Key) para continuar.")
