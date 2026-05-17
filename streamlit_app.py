import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from rag import buscar_contexto

# =========================
# CONFIGURACIÓN
# =========================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

# =========================
# PROMPT
# =========================

system_prompt = """
Eres un Tutor Socrático especializado en Bases de Datos.

Debes responder SOLO usando el contexto recuperado.

Si el contexto NO contiene la respuesta,
responde exactamente:

"No encuentro esa información en los documentos."

Nunca inventes información.
"""

configuration = types.GenerateContentConfig(
    temperature=0.3,
    max_output_tokens=1000,
    system_instruction=system_prompt
)

# =========================
# INTERFAZ
# =========================

st.set_page_config(page_title="Tutor RAG", layout="wide")

st.title("Tutor Socrático de Bases de Datos con RAG")

st.write(
    "Asistente académico basado en recuperación semántica y generación aumentada."
)

st.divider()

pregunta = st.text_input("Haz una pregunta:")

if st.button("Consultar"):

    # =========================
    # RECUPERACIÓN DE CONTEXTO
    # =========================

    contexto = buscar_contexto(pregunta)

    # =========================
    # PROMPT AUMENTADO
    # =========================

    prompt_final = f"""
    CONTEXTO:
    {contexto}

    PREGUNTA:
    {pregunta}
    """

    # =========================
    # RESPUESTA GEMINI
    # =========================

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=configuration,
        contents=prompt_final
    )

    # =========================
    # RESPUESTA FINAL
    # =========================

    st.subheader("Respuesta del Asistente")

    st.success(response.text)

    st.divider()

    # =========================
    # CONTEXTO RECUPERADO
    # =========================

    st.subheader("Contexto Recuperado")

    st.info(contexto)

    st.divider()

    # =========================
    # PROMPT AUMENTADO
    # =========================

    st.subheader("Prompt Aumentado")

    st.code(prompt_final, language="text")

    st.divider()

    # =========================
    # FUENTES CONSULTADAS
    # =========================

    st.subheader("Fuentes Consultadas")

    st.write(contexto)