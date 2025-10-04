# 🧠 Khan AI v4.0 - El Mayordomo Cuántico

Sistema de chatbot multiagente construido con FastAPI y Python. Inspirado en J.A.R.V.I.S., Skynet, Tony Stark y la inteligencia extraterrestre.

**Creado por:** zysus

---

## 🚀 Características

- ✅ **Arquitectura Multiagente**: Agentes especializados para diferentes tareas
- ✅ **Chat Inteligente**: Integración con Ollama para LLMs locales
- ✅ **Personalidad Adaptativa**: Khan aprende de tus interacciones
- ✅ **Modo Serio/Normal**: Alterna entre J.A.R.V.I.S. (sarcástico) y Skynet (crítico)
- ✅ **Base de Datos Persistente**: SQLite con aiosqlite para memoria a largo plazo
- ✅ **Interfaz Futurista**: Diseño cyber-neón con animaciones
- ✅ **Sistema de Feedback**: Khan mejora según tus respuestas
- ✅ **Proactividad**: Sugerencias automáticas en situaciones críticas

---

## 📋 Requisitos Previos

- **Windows 10 Profesional** (o superior)
- **Python 3.8+** instalado
- **Ollama** (opcional, para LLMs locales)

---

## 🔧 Instalación

### 1. Clonar o crear la estructura

Crea la carpeta principal:

```bash
mkdir C:\KhanAI
cd C:\KhanAI
```

### 2. Crear entorno virtual

```bash
python -m venv khan_env
```

### 3. Activar entorno virtual

```bash
.\khan_env\Scripts\activate
```

Verás `(khan_env)` al inicio de tu línea de comandos.

### 4. Actualizar pip

```bash
python -m pip install --upgrade pip
```

### 5. Instalar dependencias

```bash
pip install -r requirements.txt
```

**Nota:** Si hay conflictos, instala las dependencias una por una:

```bash
pip install fastapi==0.115.0
pip install uvicorn[standard]==0.32.0
pip install sqlalchemy==1.4.52
pip install aiosqlite==0.20.0
pip install python-multipart==0.0.7
pip install jinja2==3.1.4
pip install nltk==3.8.1
pip install numpy==1.24.3
pip install python-dotenv==1.0.0
```

Para Ollama (opcional):
```bash
pip install ollama==0.4.0
```

### 6. Verificar la estructura

Asegúrate de que tu estructura sea:

```
C:\KhanAI\
├── run.py
├── requirements.txt
├── README.md
├── khan_env/
└── app/
    ├── __init__.py
    ├── main.py
    ├── api/
    │   ├── __init__.py
    │   └── router.py
    ├── agents/
    │   ├── __init__.py
    │   ├── base.py
    │   └── Khan.py
    ├── core/
    │   ├── __init__.py
    │   └── simple_auth.py
    ├── db/
    │   ├── __init__.py
    │   └── database.py
    ├── models/
    │   ├── __init__.py
    │   └── user.py
    └── templates/
        ├── login.html
        ├── index.html
        ├── admin.html
        ├── css/
        │   └── style.css
        ├── js/
        │   ├── chat.js
        │   └── admin.js
        └── img/
            └── (logos, iconos, etc.)
```

### 7. Crear carpetas faltantes

```bash
mkdir app\templates\img
```

---

## ▶️ Ejecutar Khan AI

Con el entorno virtual activado:

```bash
python run.py
```

Verás algo como:

```
🚀 Iniciando Khan AI...
📡 Servidor corriendo en: http://localhost:8000
🔐 Login: http://localhost:8000/login
INFO:     Uvicorn running on http://0.0.0.0:8000
✅ Base de datos inicializada
```

---

## 🔐 Credenciales por Defecto

- **Usuario:** `zysus`
- **Contraseña:** `khan2025`

**⚠️ IMPORTANTE:** Cambia estas credenciales en `app/main.py` para producción.

---

## 🎯 Uso

### Acceder a la aplicación

1. Abre tu navegador en: `http://localhost:8000`
2. Inicia sesión con las credenciales
3. ¡Empieza a chatear con Khan!

### Modos de Khan

- **Modo Normal** 🤖: Sarcástico pero útil (J.A.R.V.I.S.)
- **Modo Serio** 🎯: Respuestas concisas y críticas (Skynet)

Khan detecta automáticamente palabras clave críticas y ajusta su tono.

### Panel de Administración

Accede a `/admin` para:
- Ver estado del sistema
- Monitorear quirks activos
- Revisar logs de interacciones
- Ajustar personalidad de Khan
- Gestionar la base de datos

---

## 🤖 Configurar Ollama (Opcional)

Si quieres usar LLMs locales:

1. Instala [Ollama](https://ollama.ai/)
2. Descarga un modelo:
   ```bash
   ollama pull llama2
   ```
3. Khan detectará automáticamente Ollama

Sin Ollama, Khan usará respuestas de fallback inteligentes.

---

## 📊 Base de Datos

Khan usa SQLite (`khan.db`) con 4 tablas:

- **quirks**: Rasgos de personalidad
- **logs**: Historial de interacciones
- **user_memory**: Preferencias de usuario
- **voice_logs**: Comandos de voz (futuro)

La base de datos se crea automáticamente al iniciar.

---

## 🎨 Personalización

### Cambiar credenciales

Edita `app/main.py`, línea ~60:

```python
if username == "TU_USUARIO" and password == "TU_PASSWORD":
```

### Ajustar personalidad

Edita `app/agents/Khan.py`, línea ~30:

```python
self.personality_traits = {
    "filosofo": 80,
    "troll": 50,
    "estratega": 60,
    "skynet_critico": 70,
    "sarcasmo": 65
}
```

### Cambiar modelo de Ollama

Edita `app/agents/Khan.py`, línea ~47:

```python
self.ollama_model = "llama3"  # o mistral, codellama, etc.
```

---

## 🐛 Solución de Problemas

### Error: "Module not found"

```bash
pip install --upgrade -r requirements.txt
```

### Error: "Address already in use"

Otro proceso está usando el puerto 8000. Cambia el puerto en `run.py`:

```python
uvicorn.run(..., port=8001)
```

### Error: "Cannot connect to Ollama"

Khan funcionará sin Ollama usando respuestas de fallback. Para conectar:

1. Verifica que Ollama esté corriendo
2. Prueba: `ollama list`
3. Reinicia Khan

### Base de datos corrupta

Elimina `khan.db` y reinicia Khan. Se recreará automáticamente.

---

## 🔄 Actualizar Khan

```bash
git pull  # Si usas Git
pip install --upgrade -r requirements.txt
```

---

## 📝 Atajos de Teclado

- **Ctrl + K**: Limpiar chat
- **Ctrl + H**: Toggle historial
- **Enter**: Enviar mensaje

---

## 🛠️ Próximas Características

- 🎤 Activación por voz ("Khan")
- 🌐 Sub-agentes especializados
- 📈 Análisis de sentimiento con NLTK
- 🔒 Autenticación JWT
- 📱 App móvil
- 🌍 Multi-idioma completo

---

## 📜 Licencia

Proyecto creado por **zysus** para uso personal y educativo.

---

## 🤝 Soporte

Si encuentras problemas:
1. Verifica la estructura de archivos
2. Revisa los logs en la consola
3. Asegúrate de que el entorno virtual esté activado

---

## 🎭 Filosofía de Khan

> "Soy tu mayordomo cuántico: sarcástico cuando puedo, serio cuando debo. Aprendo de ti, evoluciono contigo, y siempre estoy 
un paso adelante."

**¡Disfruta de Khan AI!** 🚀