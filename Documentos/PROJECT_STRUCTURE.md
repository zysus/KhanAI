# 📁 Khan AI - Estructura Completa del Proyecto

## 🌳 Árbol de Directorios

```
C:\KhanAI\
│
├── 📄 run.py                      # Archivo principal de ejecución
├── 📄 requirements.txt            # Dependencias de Python
├── 📄 README.md                   # Documentación principal
├── 📄 QUICKSTART.md               # Guía de inicio rápido
├── 📄 MAINTENANCE.md              # Guía de mantenimiento
├── 📄 PROJECT_STRUCTURE.md        # Este archivo
├── 📄 LOGO_INFO.md                # Info sobre assets visuales
├── 📄 .gitignore                  # Archivos ignorados por Git
├── 📄 install.bat                 # Instalador automático Windows
├── 📄 start_khan.bat              # Script de inicio rápido
├── 💾 khan.db                     # Base de datos (generada automáticamente)
│
├── 📁 khan_env/                   # Entorno virtual (generado)
│   ├── Scripts/
│   ├── Lib/
│   └── ...
│
└── 📁 app/                        # Aplicación principal
    ├── 📄 __init__.py             # Inicializador del módulo
    ├── 📄 main.py                 # Aplicación FastAPI principal
    │
    ├── 📁 api/                    # Módulo de API
    │   ├── 📄 __init__.py
    │   └── 📄 router.py           # Endpoints de la API
    │
    ├── 📁 agents/                 # Módulo de agentes
    │   ├── 📄 __init__.py
    │   ├── 📄 base.py             # Clase base de agentes
    │   └── 📄 Khan.py             # ⭐ Agente principal Khan
    │
    ├── 📁 core/                   # Módulo core
    │   ├── 📄 __init__.py
    │   └── 📄 simple_auth.py      # Sistema de autenticación
    │
    ├── 📁 db/                     # Módulo de base de datos
    │   ├── 📄 __init__.py
    │   └── 📄 database.py         # Gestión de BD con aiosqlite
    │
    ├── 📁 models/                 # Modelos de datos
    │   ├── 📄 __init__.py
    │   └── 📄 user.py             # Modelo de usuario
    │
    └── 📁 templates/              # Plantillas y recursos web
        ├── 📄 login.html          # Página de login
        ├── 📄 index.html          # Dashboard principal
        ├── 📄 admin.html          # Panel de administración
        │
        ├── 📁 css/
        │   └── 📄 style.css       # Estilos futuristas cyber-neón
        │
        ├── 📁 js/
        │   ├── 📄 chat.js         # Lógica del chat
        │   └── 📄 admin.js        # Lógica del panel admin
        │
        └── 📁 img/                # Imágenes y logos
            ├── favicon.ico        # (A crear)
            ├── logo.png           # (A crear)
            └── logo-small.png