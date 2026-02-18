import requests
import sys
import os
 
def verificar_configuracion():
    print("--- Verificación de Entorno Virtual ---")
    # Comprobar si estamos dentro de un entorno virtual
    if hasattr(sys, 'real_prefix') or (sys.base_prefix != sys.prefix):
        print("✅ Estado: Entorno Virtual ACTIVO.")
    else:
        print("❌ Estado: Entorno Virtual NO detectado. Por favor, actívalo.")
    # Mostrar la ruta del ejecutable de Python que se está usando
    print(f"📍 Ruta de Python: {sys.executable}")
    # Simular una pequeña petición de red para verificar conexión
    try:
        response = requests.get("https://www.google.com")
        if response.status_code == 200:
            print("🌐 Conexión a internet: OK (Google es alcanzable).")
    except Exception as e:
        print(f"⚠️ Error de conexión: {e}")
 
if __name__ == "__main__":
    verificar_configuracion()