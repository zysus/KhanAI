@echo off
chcp 65001 >nul
cls
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║            🧠 Khan AI v4.0 - Iniciando...                ║
echo ║              El Mayordomo Cuántico                       ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

:: Verificar que existe el entorno virtual
if not exist "khan_env\Scripts\activate.bat" (
    echo ❌ Entorno virtual no encontrado
    echo 💡 Ejecuta primero: install.bat
    pause
    exit /b 1
)

:: Activar entorno virtual
call khan_env\Scripts\activate.bat

:: Verificar que run.py existe
if not exist "run.py" (
    echo ❌ run.py no encontrado
    echo 💡 Asegúrate de estar en el directorio correcto: C:\KhanAI
    pause
    exit /b 1
)

echo ✅ Entorno virtual activado
echo 🚀 Iniciando servidor Khan AI...
echo.
echo ═══════════════════════════════════════════════════════════
echo     Khan estará disponible en: http://localhost:8000
echo     Login en: http://localhost:8000/login
echo ═══════════════════════════════════════════════════════════
echo.
echo 💡 Presiona Ctrl+C para detener el servidor
echo.

:: Iniciar Khan
python run.py

:: Si el servidor se detiene
echo.
echo ═══════════════════════════════════════════════════════════
echo     Khan AI se ha detenido
echo ═══════════════════════════════════════════════════════════
pause
