# 🚀 Khan AI - Quick Start Guide

## Instalación Rápida (Windows)

```bash
# 1. Descargar/clonar el proyecto en C:\KhanAI
# 2. Ejecutar instalación automática
install.bat

# 3. Iniciar Khan
start_khan.bat
```

## Instalación Manual

```bash
# Crear entorno virtual
python -m venv khan_env

# Activar entorno
.\khan_env\Scripts\activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Iniciar servidor
python run.py
```

---

## 🔐 Acceso

**URL:** http://localhost:8000

**Credenciales:**
- Usuario: `zysus`
- Password: `khan2025`

---

## 📱 Navegación

| Ruta | Descripción |
|------|-------------|
| `/login` | Página de inicio de sesión |
| `/index` | Dashboard principal / Chat |
| `/admin` | Panel de administración |
| `/logout` | Cerrar sesión |

---

## 🎯 Modos de Khan

### Modo Normal 🤖
- Tono: Sarcástico pero útil (J.A.R.V.I.S.)
- Uso: Conversaciones casuales, ayuda general
- Activa con: Click en el botón de modo

### Modo Serio 🎯
- Tono: Preciso y directo (Skynet)
- Uso: Situaciones críticas, problemas técnicos
- Se activa automáticamente con palabras clave: urgente, riesgo, error, crítico

---

## 💬 Ejemplos de Uso

### Conversación Normal
```
Usuario: "Hola Khan, ¿cómo estás?"
Khan: "Operacional al 100%. Sarcasmo: Calibrado. ¿En qué puedo asistirte?"
```

### Consulta Técnica
```
Usuario: "Necesito ayuda con un error en Python"
Khan: [Modo Normal] "Por supuesto. Cuéntame qué está pasando..."
```

### Situación Crítica
```
Usuario: "Urgente: el servidor está caído"
Khan: [Modo Serio] "Situación crítica detectada. Sugiero:
• Revisar logs del sistema
• Verificar conectividad
• Implementar rollback si es necesario"
```

---

## ⌨️ Atajos de Teclado

| Atajo | Acción |
|-------|--------|
| `Ctrl + K` | Limpiar chat |
| `Ctrl + H` | Toggle historial |
| `Enter` | Enviar mensaje |

---

## 🎛️ Panel de Administración

### Estado del Sistema
- Ver status de Khan (operacional/offline)
- Verificar conexión con Ollama
- Monitorear interacciones totales

### Personalidad
- Ajustar nivel de sarcasmo (0-100%)
- Ver quirks activos
- Activar modo serio permanente

### Base de Datos
- Ver historial de interacciones
- Limpiar datos antiguos
- Gestionar memoria de usuario

---

## 🔧 Configuración

### Cambiar Puerto

Edita `run.py`:
```python
uvicorn.run(..., port=8001)  # Cambiar 8000 a 8001
```

### Cambiar Credenciales

Edita `app/main.py` (línea ~60):
```python
if username == "nuevo_user" and password == "nueva_pass":
```

### Ajustar Personalidad

Edita `app/agents/Khan.py` (línea ~30):
```python
self.personality_traits = {
    "filosofo": 90,    # 0-100
    "troll": 30,       # 0-100
    "estratega": 80,   # 0-100
    "sarcasmo": 50     # 0-100
}
```

### Cambiar Modelo de Ollama

Edita `app/agents/Khan.py` (línea ~47):
```python
self.ollama_model = "llama3"  # o mistral, codellama, etc.
```

---

## 🐛 Troubleshooting

### Error: Puerto en uso
```bash
# Cambiar puerto en run.py o matar proceso
netstat -ano | findstr :8000
taskkill /PID [PID_NUMBER] /F
```

### Error: Módulo no encontrado
```bash
pip install --upgrade -r requirements.txt
```

### Khan no responde
1. Verifica que el servidor esté corriendo
2. Revisa la consola por errores
3. Reinicia con `Ctrl+C` y `python run.py`

### Base de datos corrupta
```bash
# Detener Khan
# Eliminar khan.db
del khan.db
# Reiniciar Khan (se recreará automáticamente)
python run.py
```

---

## 📊 API Endpoints

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/chat` | POST | Enviar mensaje a Khan |
| `/api/feedback` | POST | Enviar feedback (1-10) |
| `/api/history` | GET | Obtener historial |
| `/api/status` | GET | Estado de Khan |
| `/api/preferences` | POST | Guardar preferencias |

### Ejemplo: Chat API
```javascript
fetch('/api/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        message: "Hola Khan",
        mode: "normal"
    })
})
```

---

## 🎨 Personalización Avanzada

### Cambiar Colores (CSS)

Edita `app/templates/css/style.css` (líneas 3-10):
```css
:root {
    --primary: #00ffff;    /* Color principal */
    --secondary: #ff00ff;  /* Color secundario */
    --accent: #00ff00;     /* Color de acento */
    /* ... */
}
```

### Añadir One-Liners

Edita `app/agents/Khan.py` (líneas ~57-65):
```python
self.oneliners = [
    "Tu one-liner personalizado.",
    "Otro mensaje de cierre.",
    # ...
]
```

---

## 📈 Próximas Features

- [ ] Activación por voz
- [ ] Sub-agentes especializados
- [ ] Multi-idioma completo
- [ ] Integración con más LLMs
- [ ] App móvil
- [ ] Sistema de plugins

---

## 🆘 Soporte Rápido

**Problema común:** Khan no se inicia
```bash
# Solución:
1. cd C:\KhanAI
2. .\khan_env\Scripts\activate
3. python run.py
```

**Problema común:** Error 401 (no autenticado)
```bash
# Solución:
1. Cerrar sesión (/logout)
2. Volver a iniciar sesión (/login)
3. Borrar cookies del navegador
```

---

## 📚 Recursos

- **README.md** - Documentación completa
- **Estructura de carpetas** - Ver documento principal
- **Logs** - Consola donde ejecutas Khan

---

**¡Disfruta de Khan AI!** 🚀

*Creado por zysus*