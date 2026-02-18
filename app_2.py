import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# -------------------------------
# Cargar variables de entorno
# -------------------------------
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("No se encontró la API Key en el archivo .env")
# -------------------------------
# Inicializar cliente Gemini
# -------------------------------
client = genai.Client(api_key=API_KEY)

# -------------------------------
# System Instruction
# -------------------------------
configuration = types.GenerateContentConfig(
    max_output_tokens=2048,
    system_instruction="""
    Eres un Editor Editorial de prestigio.
    Tu trabajo es editar textos de forma clara, profesional
    y con alto nivel académico.
    """
)

# -------------------------------
# Entrada del usuario
# -------------------------------
tarea = input("Digite la tarea (resumir / profesionalizar): ").lower()
texto = input("\nDigite el texto a procesar:\n")

# -------------------------------
# Construcción del prompt
# -------------------------------
if tarea == "resumir":
    prompt = f"Realiza un resumen ejecutivo del siguiente texto:\n\n{texto}"

elif tarea == "profesionalizar":
    prompt = f"Reescribe el siguiente texto con un tono formal y técnico:\n\n{texto}"

else:
    raise ValueError("Tarea no válida. Use 'resumir' o 'profesionalizar'")

# -------------------------------
# Generar respuesta
# -------------------------------
response = client.models.generate_content(
    model="gemini-2.5-flash",
    config=configuration,
    contents=prompt
)

# -------------------------------
# Mostrar resultado
# -------------------------------
print("\n----- RESULTADO -----\n")
print(response.text)
