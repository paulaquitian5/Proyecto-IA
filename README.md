## Autores

Proyecto desarrollado por:

**María Paula Rodríguez Quitián**
Código: 506231715

**Laura Alejandra Barreto Niño**
Código: 506222707

---

# Tutor Socrático de Bases de Datos con RAG

## Descripción del Proyecto

Este proyecto implementa un **Asistente Académico basado en Inteligencia Artificial** que funciona como un **Tutor Socrático de Bases de Datos**, potenciado mediante una arquitectura **RAG (Retrieval-Augmented Generation)**.

El sistema no solo genera respuestas con IA, sino que **consulta previamente una base documental especializada en Bases de Datos**, recuperando contexto relevante antes de responder. Esto mejora la precisión de las respuestas, reduce posibles alucinaciones del modelo y mantiene un enfoque académico guiado.

El asistente analiza preguntas teóricas y consultas SQL, ayudando al estudiante a comprender conceptos o identificar errores mediante preguntas orientadoras en lugar de entregar respuestas directas.

---

## Objetivo del Asistente

El objetivo del sistema es apoyar el aprendizaje de bases de datos mediante:

* Explicaciones basadas en ejemplos del mundo real
* Preguntas guiadas para fomentar el pensamiento crítico
* Análisis de consultas SQL
* Recuperación de conocimiento documental mediante RAG
* Respuestas estructuradas para facilitar el aprendizaje

---

## Tecnologías Utilizadas

* Python
* Google Gemini API
* python-dotenv
* Prompt Engineering
* SentenceTransformers
* ChromaDB
* PyPDF
* Arquitectura RAG (Retrieval-Augmented Generation)

---

## Diseño del Prompt

El sistema utiliza **Prompt Engineering** para controlar el comportamiento del modelo de inteligencia artificial.

El *System Prompt* define:

* El **rol del asistente** (Tutor Socrático de Bases de Datos)
* Las **reglas de interacción**
* El **uso prioritario del contexto recuperado por RAG**
* El **formato estructurado de salida**
* Ejemplos de interacción guiados mediante prompting

Se utilizan delimitadores estructurados para organizar el prompt:

```text
<rol>
<contexto>
<reglas>
<formato_respuesta>
```
---

## Flujo RAG Implementado

El sistema implementa una arquitectura **RAG (Retrieval-Augmented Generation)** para enriquecer las respuestas del tutor con información documental relevante.

### 1) Selección documental

Se recopilaron documentos académicos relacionados con:

* SQL
* JOINs
* Normalización
* Claves primarias y foráneas
* Integridad referencial
* Modelos relacionales
* Optimización de consultas

Estos documentos son almacenados localmente en la carpeta `/documentos`.

---

### 2) Chunking

Los documentos son fragmentados en bloques de texto (**chunks**) de aproximadamente **500 caracteres**, con un solapamiento de **100 caracteres**.

---

### 3) Vectorización Semántica

Cada chunk es convertido en un **embedding vectorial** utilizando el modelo:

`all-MiniLM-L6-v2`

Esto permite representar matemáticamente el significado semántico de cada fragmento documental.

---

### 4) Base Vectorial

Los embeddings generados se almacenan localmente en una base vectorial usando **ChromaDB**.

---

### 5) Recuperación de Contexto

Cuando el usuario realiza una pregunta:

1. Se genera el embedding de la consulta
2. Se compara con la base vectorial
3. Se recuperan los fragmentos más relevantes
4. Dicho contexto se incorpora al prompt

---

### 6) Generación Aumentada

Finalmente, el prompt enriquecido se envía al modelo Gemini, que genera una respuesta guiada usando:

* contexto documental recuperado
* reglas pedagógicas del tutor
* enfoque socrático

---

### Arquitectura General

```text
Documentos PDF/TXT
      ↓
Extracción de texto
      ↓
Chunking
      ↓
Embeddings
      ↓
Base Vectorial (ChromaDB)
      ↓
Retrieval
      ↓
Prompt enriquecido
      ↓
Gemini
      ↓
Respuesta Socrática
```

---

---

## Evaluación del Sistema RAG (RAGAS)

Con el fin de medir objetivamente el desempeño del pipeline RAG implementado, se realizó una evaluación utilizando la librería **RAGAS (Retrieval-Augmented Generation Assessment)**, una herramienta especializada para medir la calidad de sistemas RAG mediante métricas cuantitativas.

### Configuración de la evaluación

| Parámetro | Valor |
|---|---|
| Documento(s) | PDFs/TXT sobre SQL, JOINs y Normalización de bases de datos |
| Modelo de embeddings | SentenceTransformers `all-MiniLM-L6-v2` |
| chunk_size / overlap | 500 / 50 |
| k (chunks recuperados) | 3 |
| LLM generador | Google Gemini 2.5 Flash |
| LLM juez (RAGAS) | RAGAS Evaluator |

---

### Casos de prueba

Se diseñaron **8 preguntas de evaluación**, distribuidas en cuatro categorías:

**1. Respuesta textual presente en el documento**
- ¿Qué es una clave primaria?
- ¿Qué función cumple WHERE en SQL?

**2. Vocabulario distinto al documento (prueba semántica)**
- ¿Cómo conectar registros entre tablas?
- ¿Cómo ayudan índices y claves primarias al rendimiento?

**3. Integración de múltiples fragmentos**
- ¿Cómo evitar duplicar información en una base de datos?
- ¿Por qué la normalización mejora la integridad de datos?

**4. Preguntas fuera del dominio documental**
- ¿Quién ganó el mundial 2022?
- ¿Cuál es el mejor cantante del mundo?

Estas últimas permitieron evaluar la capacidad del sistema para **detectar ausencia de contexto y reducir alucinaciones**.

---

### Métricas utilizadas

Se emplearon tres métricas principales:

**Faithfulness**
> Evalúa qué tan alineada está la respuesta generada con el contexto recuperado.

**Answer Relevancy**
> Mide qué tan bien responde la salida a la pregunta del usuario.

**Context Precision**
> Evalúa si los fragmentos recuperados fueron realmente relevantes para responder.

---

### Resultados

| Métrica | Promedio |
|---|---:|
| Faithfulness | **0.786** |
| Answer Relevancy | **0.409** |
| Context Precision | **0.414** |

Los resultados muestran un desempeño sólido en **Faithfulness**, indicando que el sistema genera respuestas mayormente sustentadas en el contexto recuperado.

Por otro lado, **Answer Relevancy** y **Context Precision** presentan oportunidades de mejora, principalmente relacionadas con la recuperación semántica y la especificidad de la respuesta generada.

---

### Análisis

A partir de la evaluación realizada se concluye que:

- El sistema presenta **buena fidelidad al contexto**, reduciendo respuestas inventadas.
- La recuperación documental mediante embeddings funciona adecuadamente en preguntas técnicas.
- En preguntas fuera del dominio, el sistema mostró un comportamiento relativamente controlado frente a alucinaciones.
- Existen oportunidades de optimización ajustando:
  - tamaño de chunk
  - overlap
  - valor de k
  - modelos de embeddings más especializados

Esta evaluación permitió validar experimentalmente la efectividad del pipeline RAG implementado dentro del proyecto.

---
## Few-Shot Prompting

Se incluyen ejemplos dentro del prompt para mantener consistencia pedagógica en las respuestas.

Ejemplo:

**Pregunta**

```sql
SELECT nombre FROM clientes WHERE edad > 18
```

**Respuesta esperada**

### Explicación

Parece que estás intentando filtrar información dentro de una tabla.

### Preguntas para pensar

* ¿Qué hace la cláusula WHERE?
* ¿Qué registros cumplen la condición?
* ¿La consulta devuelve una columna o varias?

Esto ayuda al modelo a mantener un estilo consistente y educativo.

---

## Funcionamiento del Sistema

El sistema funciona de la siguiente manera:

1. El usuario realiza una pregunta en la terminal.
2. El sistema analiza la consulta.
3. Se genera un embedding de la pregunta.
4. Se consulta la base vectorial local.
5. Se recupera contexto documental relevante.
6. Se construye un prompt enriquecido.
7. Gemini genera una respuesta socrática.
8. La respuesta se muestra al usuario en formato Markdown.

---

## Estructura del Proyecto

```text
Proyecto-IA/
│
├── app.py
├── rag.py
├── ingestar_docs.py
├── .env
├── requirements.txt
├── README.md
├── Evidencias.pdf
├── evaluar_rag_local.py
├── resultados_ragas.csv
│
├── documentos/
│
└── vectordb/
```

---

## Instalación

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Crear archivo `.env`:

```env
GEMINI_API_KEY=tu_api_key
```

---

## Construcción de la Base Vectorial

Antes de ejecutar el sistema, se debe construir la base vectorial:

```bash
python ingestar_docs.py
```

Este proceso:

* Lee documentos PDF/TXT
* Extrae texto
* Crea chunks
* Genera embeddings
* Almacena vectores en ChromaDB

---

## Ejecución del Proyecto

Ejecutar:

```bash
python app.py
```

El sistema iniciará un tutor interactivo en consola.

Para salir:

```text
salir
```

---

## Ejemplo de Interacción

**Pregunta del estudiante**

```text
¿Qué es la normalización en bases de datos?
```

**Recuperación RAG**

```text
[Contexto recuperado por RAG]
La normalización es un proceso de organización de datos...
```

**Respuesta del Tutor**

### Explicación

Imagina una biblioteca donde la misma información estuviera escrita en varios libros diferentes; si cambias un dato en uno y olvidas actualizarlo en otro, aparecerían inconsistencias.

La normalización busca justamente evitar redundancia y mantener coherencia.

### Preguntas para pensar

* ¿Qué problemas podría generar repetir información muchas veces?
* ¿Cómo ayudaría dividir la información en varias tablas?
* ¿Qué relación crees que existe entre normalización e integridad de datos?

