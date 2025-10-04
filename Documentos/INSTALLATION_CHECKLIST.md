# ✅ Khan AI - Checklist de Instalación y Verificación

## 📋 Pre-Instalación

### Requisitos del Sistema
- [ ] Windows 10 Profesional o superior
- [ ] Al menos 2GB de RAM libre
- [ ] 1GB de espacio en disco
- [ ] Conexión a internet (para instalar dependencias)

### Software Necesario
- [ ] Python 3.8 o superior instalado
  - Verificar: `python --version`
  - Descargar desde: https://python.org
- [ ] pip actualizado
  - Verificar: `pip --version`
- [ ] (Opcional) Ollama instalado
  - Descargar desde: https://ollama.ai

---

## 📁 Estructura de Archivos

### Archivos Python Principales
- [ ] `run.py` existe
- [ ] `requirements.txt` existe
- [ ] `app/__init__.py` existe
- [ ] `app/main.py` existe
- [ ] `app/agents/Khan.py` existe
- [ ] `app/api/router.py` existe
- [ ] `app/core/simple_auth.py` existe
- [ ] `app/db/database.py` existe

### Archivos HTML/CSS/JS
- [ ] `app/templates/login.html` existe
- [ ] `app/templates/index.html` existe
- [ ] `app/templates/admin.html` existe
- [ ] `app/templates/css/style.css` existe
- [ ] `app/templates/js/chat.js` existe
- [ ] `app/templates/js/admin.js` existe

### Archivos de Configuración
- [ ] `README.md` existe
- [ ] `QUICKSTART.md` existe
- [ ] `.gitignore` existe (opcional)
- [ ] `install.bat` existe
- [ ] `start_khan.bat` existe

### Carpetas Necesarias
- [ ] Carpeta `app/` existe
- [ ] Carpeta `app/api/` existe
- [ ] Carpeta `app/agents/` existe
- [ ] Carpeta `app/core/` existe
- [ ] Carpeta `app/db/` existe
- [ ] Carpeta `app/models/` existe
- [ ] Carpeta `app/templates/` existe
- [ ] Carpeta `app/templates/css/` existe
- [ ] Carpeta `app/templates/js/` existe
- [ ] Carpeta `app/templates/img/` existe

---

## 🔧 Instalación

### Paso 1: Crear Entorno Virtual
- [ ] Ejecutar: `python -m venv khan_env`
- [ ] Verificar que existe la carpeta `khan_env/`
- [ ] Verificar que existe `khan_env/Scripts/activate.bat`

### Paso 2: Activar Entorno Virtual
- [ ] Ejecutar: `.\khan_env\Scripts\activate`
- [ ] Verificar que aparece `(khan_env)` en el prompt
- [ ] Ejecutar: `python --version` (debe mostrar la versión)
- [ ] Ejecutar: `pip --version` (debe mostrar la versión)

### Paso 3: Instalar Dependencias
- [ ] Ejecutar: `pip install --upgrade pip`
- [ ] Ejecutar: `pip install -r requirements.txt`
- [ ] Verificar instalaciones:
  - [ ] `pip show fastapi` (debe mostrar versión 0.115.0)
  - [ ] `pip show uvicorn` (debe mostrar versión 0.32.0)
  - [ ] `pip show aiosqlite` (debe mostrar versión 0.20.0)
  - [ ] `pip show sqlalchemy` (debe mostrar versión 1.4.52)

### Paso 4: Verificar Instalación
- [ ] Ejecutar: `pip list` (ver todas las dependencias)
- [ ] No hay mensajes de error
- [ ] Todas las dependencias críticas instaladas

---

## 🚀 Primera Ejecución

### Iniciar el Servidor
- [ ] Entorno virtual activado
- [ ] Ejecutar: `python run.py`
- [ ] Verificar salida:
  - [ ] Mensaje: "🚀 Iniciando Khan AI..."
  - [ ] Mensaje: "✅ Base de datos inicializada"
  - [ ] Mensaje: "INFO: Uvicorn running on..."
  - [ ] Sin mensajes de error

### Verificar Base de Datos
- [ ] Archivo `khan.db` creado automáticamente
- [ ] Tamaño mayor a 0 bytes
- [ ] Sin errores de permisos

### Verificar Servidor Web
- [ ] Abrir navegador
- [ ] Ir a: `http://localhost:8000`
- [ ] Redirige a `/login`
- [ ] Página de login se muestra correctamente
- [ ] Estilos CSS cargados (página con colores cyber-neón)

---

## 🔐 Prueba de Autenticación

### Login
- [ ] Ingresar usuario: `zysus`
- [ ] Ingresar contraseña: `khan2025`
- [ ] Hacer clic en "Acceder"
- [ ] Redirige a `/index`
- [ ] Dashboard se muestra correctamente
- [ ] Mensaje de bienvenida de Khan aparece

### Verificar Sesión
- [ ] Cookie `auth_token` establecida
- [ ] Usuario mostrado en sidebar
- [ ] Botón "Salir" visible
- [ ] No hay mensajes de error 401

---

## 💬 Prueba de Chat

### Enviar Mensaje
- [ ] Escribir mensaje: "Hola Khan"
- [ ] Presionar Enter o clic en "Enviar"
- [ ] Mensaje del usuario aparece en el chat
- [ ] Indicador "Khan está pensando..." aparece
- [ ] Respuesta de Khan aparece
- [ ] Respuesta tiene sentido
- [ ] One-liner de Khan incluido (si aplica)

### Verificar Modos
- [ ] Clic en botón "Modo Normal/Serio"
- [ ] Icono cambia
- [ ] Texto cambia
- [ ] Enviar mensaje en modo serio
- [ ] Tono de respuesta cambia según modo

### Verificar Historial
- [ ] Clic en icono de historial (o Ctrl+H)
- [ ] Panel lateral de historial aparece
- [ ] Mensajes anteriores se muestran
- [ ] Fechas correctas
- [ ] Cerrar historial funciona

---

## ⚙️ Prueba del Panel Admin

### Acceder a Admin
- [ ] Ir a: `http://localhost:8000/admin`
- [ ] Página de admin se carga
- [ ] No hay errores 401 o 404

### Verificar Estado del Sistema
- [ ] Estado muestra "Operacional"
- [ ] Versión muestra "4.0"
- [ ] Estado de Ollama se muestra
- [ ] Contador de interacciones funciona

### Verificar Personalidad
- [ ] Barras de progreso visibles
- [ ] Valores correctos (80%, 50%, 60%, 65%)
- [ ] Animaciones funcionan

### Verificar Quirks
- [ ] Sección de quirks visible
- [ ] Quirks se cargan (o mensaje "No hay quirks")
- [ ] Botón de actualizar funciona

### Verificar Logs
- [ ] Tabla de logs visible
- [ ] Interacciones anteriores mostradas
- [ ] Fechas formateadas correctamente
- [ ] Colores según feedback

### Verificar Configuraciones
- [ ] Checkbox "Modo Serio" funciona
- [ ] Select de modelo Ollama funciona
- [ ] Slider de sarcasmo funciona
- [ ] Valor actualiza en tiempo real

---

## 🔄 Pruebas de Funcionalidad

### API Endpoints
- [ ] `GET /health` responde con status 200
- [ ] `GET /api/status` devuelve JSON válido
- [ ] `POST /api/chat` acepta mensajes
- [ ] `POST /api/feedback` acepta puntuaciones
- [ ] `GET /api/history` devuelve historial

### Base de Datos
- [ ] Tabla `quirks` existe
- [ ] Tabla `logs` existe
- [ ] Tabla `user_memory` existe
- [ ] Tabla `voice_logs` existe
- [ ] Datos se guardan correctamente

### Fallbacks
- [ ] Si Ollama no está disponible, Khan usa fallback
- [ ] Mensajes de fallback tienen sentido
- [ ] No hay crashes por falta de Ollama

---

## 🎨 Pruebas Visuales

### Diseño Responsive
- [ ] Página se ve bien en pantalla completa
- [ ] Sidebar visible y funcional
- [ ] Chat ocupa espacio correcto
- [ ] Scroll funciona en mensajes largos

### Animaciones
- [ ] Mensajes aparecen con animación
- [ ] Hover en botones funciona
- [ ] Indicador de estado parpadea
- [ ] Transiciones suaves

### Colores y Tema
- [ ] Colores cyber-neón correctos
- [ ] Contraste legible
- [ ] Efectos de glow visibles
- [ ] Fondo animado (login) funciona

---

## 🐛 Pruebas de Error

### Errores de Autenticación
- [ ] Login con credenciales incorrectas muestra error
- [ ] Acceso sin login redirige a `/login`
- [ ] Logout funciona correctamente

### Errores de Input
- [ ] Enviar mensaje vacío no causa error
- [ ] Mensajes muy largos se manejan bien
- [ ] Caracteres especiales funcionan

### Errores de Conexión
- [ ] Si BD no existe, se crea automáticamente
- [ ] Si servidor cae, se puede reiniciar
- [ ] Errores se muestran al usuario

---

## 📊 Verificación de Rendimiento

### Tiempo de Respuesta
- [ ] Página de login carga < 2 segundos
- [ ] Dashboard carga < 3 segundos
- [ ] Respuesta de Khan < 5 segundos (sin Ollama)
- [ ] Respuesta de Khan < 10 segundos (con Ollama)

### Uso de Recursos
- [ ] Uso de CPU < 50% en reposo
- [ ] Uso de RAM < 500MB
- [ ] Tamaño de `khan.db` razonable

---

## ✅ Checklist Final

### Funcionalidad Core
- [ ] Login/Logout funciona
- [ ] Chat funciona
- [ ] Khan responde coherentemente
- [ ] Modos Normal/Serio funcionan
- [ ] Historial funciona
- [ ] Panel admin funciona
- [ ] Base de datos funciona

### Experiencia de Usuario
- [ ] Interfaz intuitiva
- [ ] Diseño atractivo
- [ ] Sin errores visibles
- [ ] Rendimiento aceptable

### Documentación
- [ ] README.md leído
- [ ] QUICKSTART.md consultado
- [ ] Credenciales anotadas
- [ ] Comandos básicos conocidos

---

## 🎉 Post-Instalación

### Configuración Personalizada
- [ ] Cambiar credenciales por defecto (recomendado)
- [ ] Ajustar personalidad de Khan (opcional)
- [ ] Configurar Ollama si está disponible
- [ ] Crear logos personalizados (opcional)

### Backup Inicial
- [ ] Hacer backup de `khan.db`
- [ ] Documentar cambios en configuración
- [ ] Anotar credenciales en lugar seguro

### Próximos Pasos
- [ ] Explorar todas las funcionalidades
- [ ] Probar diferentes modos y consultas
- [ ] Dar feedback a Khan
- [ ] Revisar logs y quirks generados

---

## 🆘 Si Algo Falla

### Checklist de Troubleshooting
1. [ ] ¿Entorno virtual activado?
2. [ ] ¿Todas las dependencias instaladas?
3. [ ] ¿Puerto 8000 disponible?
4. [ ] ¿Estructura de archivos correcta?
5. [ ] ¿Permisos de escritura en carpeta?
6. [ ] ¿Python versión correcta?

### Comandos de Verificación
```bash
# Verificar Python
python --version

# Verificar pip
pip --version

# Verificar dependencias
pip list

# Verificar puerto
netstat -ano | findstr :8000

# Verificar estructura
dir /s /b app
```

### Reinstalación Limpia
Si todo falla:
1. [ ] Desactivar entorno: `deactivate`
2. [ ] Eliminar `khan_env/`
3. [ ] Eliminar `khan.db`
4. [ ] Ejecutar `install.bat` de nuevo

---

## 📝 Notas Finales

**Instalación completada cuando:**
✅ Todos los checkboxes marcados
✅ Sin errores críticos
✅ Khan responde correctamente
✅ Interfaz funcional

**Tiempo estimado de instalación:**
- Automática (install.bat): 5-10 minutos
- Manual: 15-20 minutos

**Problemas comunes resueltos:**
- Entorno virtual
- Dependencias
- Base de datos
- Autenticación

---

**¡Felicidades! Khan AI está listo para usar.** 🚀

*Creado por zysus - Khan AI v4.0*