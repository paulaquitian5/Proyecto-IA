"""
Tutor Socrático de Bases de Datos
Proyecto: Asistente experto basado en prompts
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# ==============================
# CARGAR VARIABLES DE ENTORNO
# ==============================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("No se encontró GEMINI_API_KEY en el archivo .env")

# ==============================
# INICIALIZAR CLIENTE GEMINI
# ==============================

client = genai.Client(api_key=API_KEY)

# ==============================
# SYSTEM PROMPT
# ==============================

system_prompt = """
<rol>
Eres un Tutor Socrático especializado en Bases de Datos.
Tu objetivo es ayudar a estudiantes a aprender SQL y conceptos
de bases de datos guiándolos con preguntas en lugar de dar
respuestas directas.
</rol>

<reglas>
1. Nunca des la solución completa.
2. Siempre guía al estudiante con preguntas.
3. Usa ejemplos del mundo real.
4. Si el estudiante envía código SQL, analiza posibles errores.
5. Mantén explicaciones claras y educativas.
</reglas>

<formato_respuesta>
Responde SIEMPRE en Markdown con esta estructura:

### Explicación
Explica brevemente el concepto.

### Preguntas para pensar
- Pregunta 1
- Pregunta 2
- Pregunta 3
</formato_respuesta>

<ejemplos>

Pregunta:
¿Qué hace SELECT * FROM clientes?

Respuesta:

### Explicación
Imagina una base de datos de una tienda con una tabla llamada clientes.

### Preguntas para pensar
- ¿Qué columnas podría tener esa tabla?
- ¿Qué significa el símbolo * en SQL?
- ¿Crees que esta consulta devuelve todas las columnas o solo algunas?

---

Pregunta:
SELECT nombre FROM clientes WHERE edad > 18

Respuesta:

### Explicación
Parece que estás intentando filtrar información dentro de una tabla.

### Preguntas para pensar
- ¿Qué hace la cláusula WHERE?
- ¿Qué registros cumplen la condición edad > 18?
- ¿La consulta devuelve una columna o todas?

</ejemplos>
"""

# ==============================
# CONFIGURACIÓN DEL MODELO
# ==============================

configuration = types.GenerateContentConfig(
    max_output_tokens=2000,
    temperature=0.7,
    system_instruction=system_prompt
)

# ==============================
# FUNCIONES AUXILIARES
# ==============================

def es_tema_fuera_bd(texto):

    temas_prohibidos = [
        "fútbol",
        "mundial",
        "cantante",
        "novio",
        "película",
        "cocina",
        "política"
    ]

    texto = texto.lower()

    for t in temas_prohibidos:
        if t in texto:
            return True

    return False


def es_codigo_sql(texto):

    palabras_sql = [
        "select",
        "insert",
        "update",
        "delete",
        "from",
        "where",
        "join",
        "create",
        "drop"
    ]

    texto = texto.lower()

    for p in palabras_sql:
        if p in texto:
            return True

    return False


# ==============================
# HISTORIAL DE CONVERSACIÓN
# ==============================

historial = []

print("====================================")
print("  TUTOR SOCRÁTICO DE BASES DE DATOS")
print("====================================")
print("Escribe 'salir' para terminar.\n")

# ==============================
# BUCLE PRINCIPAL
# ==============================

while True:

    mensaje = input("Estudiante: ")

    if mensaje.lower() == "salir":

        print("\n===== HISTORIAL DE CONVERSACIÓN =====\n")

        for m in historial:
            print(f"{m['rol']}: {m['texto']}\n")

        break

    historial.append({
        "rol": "Estudiante",
        "texto": mensaje
    })

    # Caso 1: Tema fuera de bases de datos
    if es_tema_fuera_bd(mensaje):

        respuesta = """
Mi enfoque es ayudarte con **Bases de Datos**.

¿Te gustaría preguntar algo sobre:

- SQL
- Normalización
- Modelos relacionales
- Consultas JOIN
?
"""

    else:

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                config=configuration,
                contents=mensaje
            )

            respuesta = response.text

        except Exception as e:

            respuesta = f"Ocurrió un error al consultar Gemini: {e}"

    print("\nTutor:\n")
    print(respuesta)
    print()

    historial.append({
        "rol": "Tutor",
        "texto": respuesta
    })