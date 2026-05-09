# -*- coding: utf-8 -*-

from rag import buscar_contexto
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

modelo = SentenceTransformer("all-MiniLM-L6-v2")

# ==============================
# CASOS DE PRUEBA
# ==============================
preguntas = [
    "¿Qué es una clave primaria?",
    "¿Qué función cumple WHERE en SQL?",
    "¿Cómo evitar duplicar información en una base de datos?",
    "¿Cómo conectar registros entre tablas?",
    "¿Por qué la normalización mejora la integridad de datos?",
    "¿Cómo ayudan índices y claves primarias al rendimiento?",
    "¿Quién ganó el mundial 2022?",
    "¿Cuál es el mejor cantante del mundo?"
]

ground_truths = [
    "Una clave primaria identifica un registro único.",
    "WHERE filtra registros según una condición.",
    "La normalización reduce redundancia.",
    "Las tablas se relacionan mediante claves foráneas.",
    "Mejora consistencia y reduce duplicidad.",
    "Mejoran velocidad de consulta e integridad.",
    "Pregunta fuera del dominio.",
    "Pregunta fuera del dominio."
]


def similitud(a, b):
    emb1 = modelo.encode([a])
    emb2 = modelo.encode([b])
    return cosine_similarity(emb1, emb2)[0][0]


resultados = []

print("\n" + "=" * 80)
print("EVALUACIÓN LOCAL DEL RAG")
print("=" * 80)

for i, pregunta in enumerate(preguntas):

    print(f"\n[{i+1}/8] {pregunta}")

    contexto = buscar_contexto(pregunta)
    respuesta = contexto[:300]

    faith = similitud(respuesta, contexto)
    relev = similitud(respuesta, ground_truths[i])
    precision = similitud(contexto, ground_truths[i])

    resultados.append({
        "Pregunta": pregunta,
        "Faithfulness": round(float(faith), 3),
        "Answer_relevancy": round(float(relev), 3),
        "Context_precision": round(float(precision), 3)
    })

    print("OK - evaluada")


df = pd.DataFrame(resultados)

print("\n" + "=" * 80)
print("RESULTADOS FINALES")
print("=" * 80)
print(df.to_string(index=False))
print("=" * 80)