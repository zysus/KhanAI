"""
Khan AI - Sistema de Chatbot Multiagente
Creado por zysus
"""
import uvicorn
import sys
import os

# Añadir el directorio raíz al path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Verificar que la estructura existe
app_dir = os.path.join(current_dir, 'app')
if not os.path.exists(app_dir):
    print("❌ Error: No se encuentra la carpeta 'app/'")
    print(f"   Buscando en: {app_dir}")
    input("Presiona Enter para salir...")
    sys.exit(1)

main_file = os.path.join(app_dir, 'main.py')
if not os.path.exists(main_file):
    print("❌ Error: No se encuentra 'app/main.py'")
    print(f"   Buscando en: {main_file}")
    input("Presiona Enter para salir...")
    sys.exit(1)

# Verificar __init__.py
init_file = os.path.join(app_dir, '__init__.py')
if not os.path.exists(init_file):
    print("⚠️  Advertencia: Falta app/__init__.py, creándolo...")
    with open(init_file, 'w') as f:
        f.write('# Khan AI\n__version__ = "4.0"\n')

if __name__ == "__main__":
    print("🚀 Iniciando Khan AI...")
    print("📡 Servidor corriendo en: http://localhost:8000")
    print("🔐 Login: http://localhost:8000/login")
    print("")
    
    try:
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Error al iniciar: {e}")
        input("Presiona Enter para salir...")
        sys.exit(1)
