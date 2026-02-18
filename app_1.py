"""
Ejercicio 1: Conexión y Petición Básica
Desarrollo de aplicaciones con IA
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Cargar variables de entorno
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("No se encontró la API Key en el archivo .env")

# Inicializar cliente
client = genai.Client(api_key=API_KEY)

# System Instruction (como en clase)
configuration = types.GenerateContentConfig(
    max_output_tokens=300,
    system_instruction="""
Eres un asistente académico especializado en Inteligencia Artificial.
Responde de forma clara, concisa y con menos de 50 palabras.
"""
)

# Entrada del usuario
prompt = "¿Qué es la inferencia en Inteligencia Artificial?"

# Petición al modelo (EL MODELO DE CLASE)
response = client.models.generate_content(
    model="gemini-2.5-flash",
    config=configuration,
    contents=prompt
)

print("Respuesta del modelo:")
print(response.text)
