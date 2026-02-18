import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Cargar variables de entorno
load_dotenv()
API_KEY = os.getenv("GENAI_API_KEY")

# Inicializar cliente
client = genai.Client(api_key=API_KEY)

# Configuración del sistema (ROL)
configuration = types.GenerateContentConfig(
    max_output_tokens=2048,
    system_instruction="""
    Eres un vendedor amable de una tienda de tecnología.
    Respondes de manera clara, amigable y profesional.
    Proporcionas especificaciones técnicas básicas de los productos.
    """
)

# Crear el chat con historial (FEW-SHOT)
chat = client.chats.create(
    model="gemini-2.5-flash",
    config=configuration,
    history=[
        types.Content(
            role="user",
            parts=[types.Part(text="¿Qué especificaciones tiene el iPhone 14?")]
        ),
        types.Content(
            role="model",
            parts=[types.Part(text="""
El iPhone 14 cuenta con:
- Pantalla Super Retina XDR de 6.1 pulgadas
- Chip A15 Bionic
- Cámara dual de 12 MP
- 128GB, 256GB y 512GB de almacenamiento
- Compatible con 5G
Es un excelente equipo si buscas rendimiento y buena cámara 😊
""")]
        ),
        types.Content(
            role="user",
            parts=[types.Part(text="¿Qué me puedes decir del portátil Lenovo IdeaPad 3?")]
        ),
        types.Content(
            role="model",
            parts=[types.Part(text="""
El Lenovo IdeaPad 3 incluye:
- Procesador Intel Core i5
- 8GB de RAM
- Disco SSD de 512GB
- Pantalla de 15.6 pulgadas Full HD
Es ideal para estudio, trabajo y tareas cotidianas.
""")]
        ),
    ]
)

print("--- Chat de Soporte - Tienda de Tecnología ---")
print("(Escribe 'finalizar' para terminar)\n")

# Bucle del chat
while True:
    user_input = input("Cliente: ")

    if user_input.lower() == "finalizar":
        print("Vendedor: ¡Gracias por visitar nuestra tienda! 😊 ¡Que tengas un excelente día!")
        break

    try:
        response = chat.send_message(user_input)
        print(f"\nVendedor: {response.text}\n")

    except Exception as e:
        print(f"Error al procesar la solicitud: {e}")
