
@echo off
chcp 65001 >nul
echo ╔══════════════════════════════════════════════════════════╗
echo ║         Khan AI v4.0 - Instalación Automática            ║
echo ║              El Mayordomo Cuántico                       ║
echo ║                 Creado por zysus                         ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

:: Verificar si Python está instalado
echo [1/6] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python no está instalado. Por favor instala Python 3.8+ desde python.org
    pause
    exit /b 1
)
echo ✅ Python encontrado
echo.

:: Crear entorno virtual
echo [2/6] Creando entorno virtual...
if exist khan_env (
    echo ⚠️  Entorno virtual ya existe. Eliminando...
    rmdir /s /q khan_env
)
python -m venv khan_env
if %errorlevel% neq 0 (
    echo ❌ Error creando entorno virtual
    pause
    exit /b 1
)
echo ✅ Entorno virtual creado
echo.

:: Activar entorno virtual
echo [3/6] Activando entorno virtual...
call khan_env\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ❌ Error activando entorno virtual
    pause
    exit /b 1
)
echo ✅ Entorno virtual activado
echo.

:: Actualizar pip
echo [4/6] Actualizando pip...
python -m pip install --upgrade pip --quiet
if %errorlevel% neq 0 (
    echo ⚠️  Advertencia: No se pudo actualizar pip
) else (
    echo ✅ pip actualizado
)
echo.

:: Instalar dependencias
echo [5/6] Instalando dependencias...
echo Este paso puede tardar varios minutos...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo ❌ Error instalando dependencias
    echo Intentando instalación individual...
    pip install fastapi==0.115.0
    pip install uvicorn[standard]==0.32.0
    pip install sqlalchemy==1.4.52
    pip install aiosqlite==0.20.0
    pip install python-multipart==0.0.7
    pip install jinja2==3.1.4
    pip install nltk==3.8.1
    pip install numpy==1.24.3
    pip install python-dotenv==1.0.0
    echo ⚠️  Ollama es opcional, instalando...
    pip install ollama==0.4.0
)
echo ✅ Dependencias instaladas
echo.

:: Crear carpetas necesarias
echo [6/6] Creando estructura de carpetas...
if not exist "app\templates\img" mkdir app\templates\img
if not exist "app\templates\css" mkdir app\templates\css
if not exist "app\templates\js" mkdir app\templates\js
echo ✅ Carpetas creadas
echo.

:: Resumen
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║              ✅ INSTALACIÓN COMPLETADA ✅                ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo 📝 Credenciales por defecto:
echo    Usuario: zysus
echo    Contraseña: khan2025
echo.
echo 🚀 Para iniciar Khan AI:
echo    1. Ejecuta: start_khan.bat
echo    2. O manualmente: python run.py
echo.
echo 🌐 URL: http://localhost:8000
echo.
echo 📚 Lee el README.md para más información
echo.
pause
