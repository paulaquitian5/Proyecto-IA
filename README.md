## Autores

Proyecto desarrollado por:

**María Paula Rodríguez Quitián**
Código: 506231715

**Laura Alejandra Barreto Niño**
Código: 506222707

# Tutor Socrático de Bases de Datos

## Descripción del Proyecto

Este proyecto implementa un **Asistente Académico basado en Inteligencia Artificial** que funciona como un **Tutor Socrático de Bases de Datos**.

El sistema utiliza un modelo de IA para guiar al estudiante en el aprendizaje de conceptos de bases de datos y SQL mediante preguntas y ejemplos, en lugar de proporcionar respuestas directas.

El asistente analiza preguntas teóricas y consultas SQL, ayudando al estudiante a identificar errores o comprender conceptos de manera guiada.

---

## Objetivo del Asistente

El objetivo del sistema es apoyar el aprendizaje de bases de datos mediante:

* Explicaciones basadas en ejemplos del mundo real
* Preguntas guiadas para fomentar el pensamiento crítico
* Análisis de consultas SQL
* Respuestas estructuradas para facilitar el aprendizaje

---

## Tecnologías Utilizadas

* **Python**
* **Google Gemini API**
* **python-dotenv**
* **Prompt Engineering**

---

## Diseño del Prompt

El sistema utiliza **Prompt Engineering** para controlar el comportamiento del modelo de inteligencia artificial.

El *System Prompt* define:

* El **rol del asistente** (Tutor Socrático de Bases de Datos)
* Las **reglas de interacción**
* El **formato de salida**
* Ejemplos de interacción mediante **Few-Shot Prompting**

Se utilizan **delimitadores estructurados** para organizar el prompt:

```
<rol>
<reglas>
<formato_respuesta>
<ejemplos>
```

Esto permite separar claramente:

* Instrucciones del sistema
* Ejemplos de uso
* Estructura de las respuestas

---

## Few-Shot Prompting

Se incluyeron ejemplos dentro del prompt para guiar al modelo sobre cómo debe responder.

Ejemplo incluido en el prompt:

Pregunta:
¿Qué hace SELECT * FROM clientes?

Respuesta esperada:

### Explicación

Imagina una base de datos de una tienda con una tabla llamada clientes.

### Preguntas para pensar

* ¿Qué columnas podría tener esa tabla?
* ¿Qué significa el símbolo * en SQL?
* ¿Crees que esta consulta devuelve todas las columnas o solo algunas?

Esto ayuda al modelo a mantener un **estilo consistente en las respuestas**.

---

## Funcionamiento del Sistema

El sistema funciona de la siguiente manera:

1. El usuario ingresa una pregunta en la terminal.
2. El programa analiza si el mensaje contiene código SQL o una pregunta teórica.
3. La pregunta se envía al modelo de inteligencia artificial.
4. El modelo genera una respuesta siguiendo las reglas del tutor socrático.
5. La respuesta se muestra en la terminal en formato Markdown.

---

## Estructura del Proyecto

```
taller/
│
├── app.py
├── .env
├── requirements.txt
├── README.md
└── Evidencias.pdf
```

---

## Instalación

Instalar las dependencias necesarias:

```
pip install -r requirements.txt
```

Crear un archivo `.env` con la API Key:

```
GEMINI_API_KEY=tu_api_key
```

---

## Ejecución del Proyecto

Para ejecutar el asistente:

```
python app.py
```

El sistema iniciará un tutor interactivo en la terminal.

Para finalizar la conversación escribir:

```
salir
```

---

## Ejemplo de Interacción

**Pregunta del estudiante**

```
SELECT * FROM clientes
```

**Respuesta del tutor**

### Explicación

Imagina que la tabla clientes es como una hoja de cálculo con información de clientes.

### Preguntas para pensar

* ¿Qué significa la palabra SELECT?
* ¿Qué representa el símbolo * en SQL?
* ¿Qué datos esperas ver como resultado?
