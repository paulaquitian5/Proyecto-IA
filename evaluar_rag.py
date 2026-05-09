import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from rag import buscar_contexto

from datasets import Dataset
from ragas import evaluate
from ragas.metrics.collections import (
    faithfulness,
    answer_relevancy,
    context_precision
)

import pandas as pd

import time


# ==========================
# conifg
# ==========================
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

system_prompt = """
Eres un evaluador académico de Bases de Datos.
Responde únicamente usando el contexto recuperado.
Si la pregunta está fuera del dominio, indícalo claramente.
"""

configuration = types.GenerateContentConfig(
    max_output_tokens=1000,
    temperature=0.3,
    system_instruction=system_prompt
)


# ==========================
# preguntas
# ==========================
preguntas = [
    "¿Qué es una clave primaria?",
    "¿Qué función cumple WHERE en SQL?",
    "¿Cómo evitar duplicar información en una base de datos?",
    "¿Cómo se relacionan registros entre tablas?",
    "¿Por qué la normalización mejora la integridad de datos?",
    "¿Cómo influyen índices y claves primarias en el rendimiento?",
    "¿Quién ganó el mundial 2022?",
    "¿Cuál es el mejor cantante del mundo?"
]

ground_truths = [
    "Una clave primaria identifica un registro único.",
    "WHERE filtra registros por condición.",
    "La normalización evita redundancia.",
    "Se relacionan mediante claves foráneas o JOIN.",
    "Reduce redundancia y mejora consistencia.",
    "Mejoran eficiencia de búsqueda.",
    "Pregunta fuera del dominio.",
    "Pregunta fuera del dominio."
]


# ==========================
# generar respuestas
# ==========================
answers = []
contexts = []

for pregunta in preguntas:
    print(f"Evaluando: {pregunta}")

    contexto = buscar_contexto(pregunta)

    prompt = f"""
CONTEXTO:
{contexto}

PREGUNTA:
{pregunta}
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=configuration,
        contents=prompt
    )

    respuesta = response.text

    answers.append(respuesta)
    contexts.append(contexto.split("\n\n"))
    
    time.sleep(15) # para evitar límites de tasa de la API


# ==========================
# dataset
# ==========================
dataset = Dataset.from_dict({
    "question": preguntas,
    "answer": answers,
    "contexts": contexts,
    "ground_truth": ground_truths
})


# ==========================
# evaluar
# ==========================
resultado = evaluate(
    dataset=dataset,
    metrics=[
        faithfulness(),
        answer_relevancy(),
        context_precision()
    ]
)

df = resultado.to_pandas()
df["Analisis"] = ""

df.to_excel("evaluacion_rag.xlsx", index=False)

print(df)
print("\nArchivo generado: evaluacion_rag.xlsx")