"""
Tutor Socrático de Bases de Datos
Proyecto: Asistente experto basado en prompts + RAG
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from rag import buscar_contexto

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

<contexto>
Primero debes analizar el contexto documental recuperado por el sistema RAG.

Usa esa información como base principal de tu respuesta.

Si el contexto no contiene suficiente información,
puedes complementar con conocimiento general de Bases de Datos,
manteniendo siempre el enfoque educativo y socrático.
</contexto>


<reglas>
1. Nunca des la solución completa.
2. Siempre guía al estudiante con preguntas.
3. Usa ejemplos del mundo real.
4. Si el estudiante envía código SQL, analiza posibles errores.
5. Mantén explicaciones claras y educativas.
6. Prioriza la información del contexto recuperado.
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

    for palabra in palabras_sql:
        if palabra in texto:
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

    # Caso: tema fuera de BD
    if es_tema_fuera_bd(mensaje):

        respuesta = """
Mi enfoque es ayudarte con **Bases de Datos**.

¿Te gustaría preguntar algo sobre:

- SQL
- Normalización
- Modelos relacionales
- Consultas JOIN
- Optimización de consultas
?
"""

    else:

        try:
            # ==============================
            # RECUPERAR CONTEXTO DEL RAG
            # ==============================
            contexto = buscar_contexto(mensaje)
            print("\n[Contexto recuperado por RAG]")
            print(contexto[:500])
            print("...\n")
            
            # guardar pequeño contexto conversacional
            ultimo_contexto = ""

            if len(historial) >= 2:
                ultimo_contexto = f"""
            CONVERSACIÓN PREVIA:
            Usuario: {historial[-2]["texto"]}
            """

            prompt_final = f"""
            CONTEXTO DOCUMENTAL:
            {contexto}
            {ultimo_contexto}
            
            PREGUNTA DEL ESTUDIANTE:
            {mensaje}
            """

            # ==============================
            # CONSULTAR GEMINI
            # ==============================
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                config=configuration,
                contents=prompt_final
            )

            respuesta = response.text

        except Exception as e:
            respuesta = f"Ocurrió un error al consultar el sistema RAG/Gemini: {e}"

    print("\nTutor:\n")
    print(respuesta)
    print()

    historial.append({
        "rol": "Tutor",
        "texto": respuesta

    })