# Archivo: test_render_openai.py
# Propósito: Script simple para probar la conexión a OpenAI desde Render.

import streamlit as st
import os
from openai import OpenAI, APIError, AuthenticationError, RateLimitError, APIConnectionError

st.set_page_config(page_title="Prueba OpenAI en Render", layout="centered")
st.title("🧪 Prueba de Conexión a OpenAI en Render")

# --- 1. Obtener la Clave API desde Variables de Entorno ---
# En Render, debes configurar esta variable en el dashboard del servicio.
api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    st.error("¡Error Crítico! La variable de entorno 'OPENAI_API_KEY' no está configurada en Render.")
    st.info("Ve a tu servicio en Render -> Environment y añade la variable OPENAI_API_KEY con tu clave.")
    st.stop() # Detener la ejecución si no hay clave
else:
    st.success("Variable de entorno OPENAI_API_KEY encontrada.")

# --- 2. Botón para iniciar la prueba ---
st.markdown("---")
st.write("Presiona el botón para intentar conectar y hacer una llamada simple a la API de OpenAI.")

if st.button("Realizar Prueba de Conexión"):

    # --- 3. Inicializar Cliente y Realizar Llamada ---
    with st.spinner("Intentando conectar y llamar a OpenAI..."):
        try:
            # Inicializar cliente
            st.write("- Inicializando cliente OpenAI...")
            client = OpenAI(api_key=api_key)
            st.write("- Cliente inicializado.")

            # Parámetros de prueba
            test_model = "gpt-3.5-turbo" # Modelo estándar para prueba básica
            test_prompt = "Confirma que la conexión funciona respondiendo solo con la palabra 'CONECTADO'."
            st.write(f"- Llamando al modelo: {test_model}...")

            # Llamada a la API
            response = client.chat.completions.create(
                model=test_model,
                messages=[
                    {"role": "user", "content": test_prompt}
                ],
                temperature=0.5,
                max_tokens=20
            )

            # Mostrar resultado exitoso
            st.write("- Llamada completada.")
            st.balloons()
            st.success("¡Conexión y llamada a OpenAI exitosa desde Render!")
            if response.choices:
                message_content = response.choices[0].message.content
                st.subheader("Respuesta del Modelo:")
                st.text_area("Contenido", message_content, height=100)
            else:
                st.warning("La respuesta de la API no tuvo contenido ('choices').")

        # --- Manejo de Errores Específicos ---
        except AuthenticationError:
            st.error("Error de Autenticación (AuthenticationError): Verifica que tu API Key de OpenAI sea correcta y esté activa en las variables de entorno de Render.")
        except RateLimitError:
            st.error("Error de Límite de Tasa (RateLimitError): Has excedido tu cuota de uso de la API. Espera o revisa tu plan en OpenAI.")
        except APIConnectionError:
             st.error("Error de Conexión (APIConnectionError): No se pudo establecer conexión con los servidores de OpenAI desde Render. Podría ser un problema de red temporal o de configuración.")
        except APIError as e:
            st.error(f"Error en la API de OpenAI (APIError): {e}")
        except Exception as e:
            st.error(f"Ocurrió un error inesperado general: {e}")

else:
    st.info("Esperando para iniciar la prueba...")
