# 🔧 Khan AI - Guía de Mantenimiento

## 📊 Gestión de Base de Datos

### Ver estadísticas de la BD

```python
# Ejecutar en Python interactivo con entorno activado
import aiosqlite
import asyncio

async def stats():
    async with aiosqlite.connect('khan.db') as db:
        # Contar quirks
        async with db.execute("SELECT COUNT(*) FROM quirks") as cursor:
            quirks = await cursor.fetchone()
            print(f"Quirks: {quirks[0]}")
        
        # Contar logs
        async with db.execute("SELECT COUNT(*) FROM logs") as cursor:
            logs = await cursor.fetchone()
            print(f"Logs: {logs[0]}")
        
        # Contar memoria de usuario
        async with db.execute("SELECT COUNT(*) FROM user_memory") as cursor:
            memory = await cursor.fetchone()
            print(f"User Memory: {memory[0]}")

asyncio.run(stats())
```

### Limpiar logs antiguos (manual)

```sql
-- Ejecutar con SQLite Browser o similar
DELETE FROM logs WHERE julianday('now') - julianday(timestamp) > 30;
DELETE FROM quirks WHERE julianday('now') - julianday(timestamp) > 14;
```

### Backup de la BD

```bash
# Crear backup
copy khan.db khan_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%.db

# O en PowerShell
Copy-Item khan.db -Destination "khan_backup_$(Get-Date -Format 'yyyyMMdd').db"
```

### Restaurar backup

```bash
# Detener Khan
# Reemplazar khan.db con el backup
copy khan_backup_20250103.db khan.db
# Reiniciar Khan
```

---

## 🔄 Actualización de Dependencias

### Verificar versiones actuales

```bash
pip list
```

### Actualizar todas las dependencias

```bash
pip install --upgrade -r requirements.txt
```

### Actualizar dependencias individuales

```bash
pip install --upgrade fastapi
pip install --upgrade uvicorn
```

### Verificar dependencias obsoletas

```bash
pip list --outdated
```

---

## 📝 Logs del Sistema

### Ver logs en tiempo real (Windows)

```bash
# En PowerShell
Get-Content khan.log -Wait -Tail 50
```

### Guardar logs en archivo

Edita `run.py`:
```python
import logging

logging.basicConfig(
    filename='khan.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

---

## 🧹 Limpieza del Sistema

### Script de limpieza (cleanup.bat)

```batch
@echo off
echo Limpiando archivos temporales...

:: Eliminar archivos .pyc
for /r %%i in (*.pyc) do del "%%i"

:: Eliminar __pycache__
for /d /r %%i in (__pycache__) do rd /s /q "%%i"

:: Limpiar logs antiguos (opcional)
:: del /q khan.log

echo Limpieza completada
pause
```

### Comando manual de limpieza

```bash
# Activar entorno
.\khan_env\Scripts\activate

# Ejecutar limpieza de Python
python -m pip cache purge
```

---

## 🔒 Seguridad

### Cambiar credenciales de admin

1. Edita `app/main.py` (línea ~60):
```python
if username == "TU_NUEVO_USUARIO" and password == "TU_NUEVA_PASSWORD":
```

2. Reinicia Khan

### Implementar hash de contraseñas (recomendado)

Instala bcrypt:
```bash
pip install bcrypt
```

Edita `app/core/simple_auth.py`:
```python
import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())
```

### Añadir HTTPS (producción)

```python
# En run.py
uvicorn.run(
    "app.main:app",
    host="0.0.0.0",
    port=443,
    ssl_keyfile="./key.pem",
    ssl_certfile="./cert.pem"
)
```

---

## 📈 Monitoreo de Rendimiento

### Ver uso de memoria

```python
# Añadir en app/main.py
import psutil
import os

@app.get("/system/memory")
async def memory_usage():
    process = psutil.Process(os.getpid())
    memory_mb = process.memory_info().rss / 1024 / 1024
    return {"memory_mb": round(memory_mb, 2)}
```

### Tiempo de respuesta

```python
# Middleware en app/main.py
import time

@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

---

## 🔄 Tareas Programadas

### Limpieza automática de DB (Windows Task Scheduler)

Crea un archivo `scheduled_cleanup.py`:
```python
import asyncio
from app.db.database import cleanup_old_quirks, apply_decay

async def main():
    await cleanup_old_quirks()
    await apply_decay()
    print("Limpieza automática completada")

if __name__ == "__main__":
    asyncio.run(main())
```

Programa en Task Scheduler:
- Programa: `C:\KhanAI\khan_env\Scripts\python.exe`
- Argumentos: `C:\KhanAI\scheduled_cleanup.py`
- Frecuencia: Semanal

---

## 🐛 Debugging

### Modo Debug

Edita `run.py`:
```python
uvicorn.run(
    "app.main:app",
    host="0.0.0.0",
    port=8000,
    reload=True,
    log_level="debug"  # Cambiar a debug
)
```

### Ver requests HTTP

```python
# Middleware en app/main.py
@app.middleware("http")
async def log_requests(request, call_next):
    print(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    print(f"Response: {response.status_code}")
    return response
```

### Errores comunes y soluciones

| Error | Causa | Solución |
|-------|-------|----------|
| `ImportError: No module named 'app'` | Path incorrecto | Ejecuta desde C:\KhanAI |
| `sqlite3.OperationalError: database is locked` | Múltiples conexiones | Cierra otras instancias de Khan |
| `OSError: [WinError 10048] Address already in use` | Puerto ocupado | Cambia puerto en run.py |
| `AttributeError: module 'ollama' has no attribute 'chat'` | Ollama no instalado | `pip install ollama` |

---

## 📦 Despliegue en Producción

### Requisitos adicionales

```bash
pip install gunicorn  # Para Linux
pip install python-dotenv
```

### Variables de entorno (.env)

```env
KHAN_ENV=production
KHAN_PORT=8000
KHAN_HOST=0.0.0.0
KHAN_SECRET_KEY=tu_clave_secreta_aqui
OLLAMA_HOST=http://localhost:11434
```

### Ejecutar en producción

```bash
# Con Uvicorn (Windows/Linux)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Con Gunicorn (Linux)
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

---

## 🔄 Git Workflow (Opcional)

### Inicializar repo

```bash
git init
git add .
git commit -m "Initial commit - Khan AI v4.0"
```

### Crear branches

```bash
git checkout -b feature/nueva-caracteristica
# Hacer cambios
git add .
git commit -m "Add: nueva característica"
git checkout main
git merge feature/nueva-caracteristica
```

---

## 📊 Métricas Recomendadas

Considera agregar:
- Número de usuarios activos
- Mensajes procesados por día
- Tiempo promedio de respuesta
- Score de satisfacción promedio
- Tasa de error

---

## 🆘 Recuperación de Desastres

### Khan no arranca

1. Verificar Python: `python --version`
2. Verificar entorno: `.\khan_env\Scripts\activate`
3. Reinstalar dependencias: `pip install -r requirements.txt`
4. Verificar estructura de carpetas

### BD corrupta

1. Backup actual: `copy khan.db khan_corrupt.db`
2. Eliminar DB: `del khan.db`
3. Reiniciar Khan (se recrea automáticamente)
4. Restaurar data importante manualmente

### Pérdida de configuración

Todos los archivos de configuración están en:
- `app/main.py` - Credenciales
- `app/agents/Khan.py` - Personalidad
- `app/templates/css/style.css` - Estilos

---

## 📞 Contacto y Soporte

**Creador:** zysus
**Versión:** 4.0
**Fecha:** 2025

Para reportar bugs o sugerir mejoras, documenta:
1. Versión de Khan
2. Versión de Python
3. Sistema operativo
4. Descripción del error
5. Pasos para reproducir

---

**¡Mantén a Khan funcionando sin problemas!** 🚀