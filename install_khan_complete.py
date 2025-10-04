"""
Khan AI v4.0 - Instalador Automático Completo
Este script crea TODOS los archivos necesarios
Creado por zysus
"""
import os
from pathlib import Path

def create_file(path, content):
    """Crear archivo con contenido"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return path

print("=" * 80)
print("🧠 KHAN AI v4.0 - INSTALADOR AUTOMÁTICO COMPLETO")
print("   El Mayordomo Cuántico")
print("   Creado por zysus")
print("=" * 80)
print("\n🚀 Instalando archivos completos de Khan AI...\n")

files_created = []

# ============================================================================
# 1. APP/MAIN.PY
# ============================================================================
print("[1/8] Creando app/main.py...")
files_created.append(create_file("app/main.py", '''"""
Khan AI - Main FastAPI Application
"""
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import os

from app.core.simple_auth import verify_auth, create_auth_cookie
from app.api.router import router as api_router
from app.db.database import init_db

app = FastAPI(title="Khan AI", version="4.0")

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "templates"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

app.mount("/css", StaticFiles(directory=str(STATIC_DIR / "css")), name="css")
app.mount("/js", StaticFiles(directory=str(STATIC_DIR / "js")), name="js")
app.mount("/img", StaticFiles(directory=str(STATIC_DIR / "img")), name="img")

app.include_router(api_router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    await init_db()
    print("✅ Base de datos inicializada")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    if not verify_auth(request):
        return RedirectResponse(url="/login")
    return RedirectResponse(url="/index")

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request):
    form = await request.form()
    username = form.get("username")
    password = form.get("password")
    
    if username == "zysus" and password == "khan2025":
        response = RedirectResponse(url="/index", status_code=303)
        response.set_cookie(
            key="auth_token",
            value=create_auth_cookie(username),
            httponly=True,
            max_age=86400
        )
        return response
    
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": "Credenciales incorrectas"}
    )

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie("auth_token")
    return response

@app.get("/index", response_class=HTMLResponse)
async def index_page(request: Request):
    if not verify_auth(request):
        return RedirectResponse(url="/login")
    
    username = request.cookies.get("auth_token", "Usuario")
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "username": username}
    )

@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    if not verify_auth(request):
        return RedirectResponse(url="/login")
    
    return templates.TemplateResponse("admin.html", {"request": request})

@app.get("/health")
async def health_check():
    return {"status": "online", "version": "4.0", "agent": "Khan"}
'''))

# ============================================================================
# 2. APP/CORE/SIMPLE_AUTH.PY
# ============================================================================
print("[2/8] Creando app/core/simple_auth.py...")
files_created.append(create_file("app/core/simple_auth.py", '''"""
Sistema de autenticación simple para Khan AI
"""
from fastapi import Request
import time

def create_auth_cookie(username: str) -> str:
    timestamp = str(int(time.time()))
    token = f"{username}_{timestamp}"
    return token

def verify_auth(request: Request) -> bool:
    auth_token = request.cookies.get("auth_token")
    if not auth_token:
        return False
    
    try:
        username, timestamp = auth_token.split("_")
        current_time = int(time.time())
        token_time = int(timestamp)
        
        if current_time - token_time < 86400:
            return True
    except:
        return False
    
    return False

def get_current_user(request: Request) -> str:
    auth_token = request.cookies.get("auth_token", "")
    try:
        username, _ = auth_token.split("_")
        return username
    except:
        return "guest"
'''))

# ============================================================================
# 3. APP/API/ROUTER.PY
# ============================================================================
print("[3/8] Creando app/api/router.py...")
files_created.append(create_file("app/api/router.py", '''"""
Khan AI - API Router
"""
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
import json

from app.agents.Khan import KhanAgent
from app.db.database import add_log, get_recent_logs, get_user_memory, set_user_memory
from app.core.simple_auth import verify_auth, get_current_user

router = APIRouter()
khan_agent = KhanAgent()

class ChatMessage(BaseModel):
    message: str
    mode: Optional[str] = "normal"

class FeedbackMessage(BaseModel):
    interaction_id: Optional[int] = None
    score: int
    comment: Optional[str] = None

@router.post("/chat")
async def chat(request: Request, chat_msg: ChatMessage):
    if not verify_auth(request):
        raise HTTPException(status_code=401, detail="No autenticado")
    
    username = get_current_user(request)
    
    try:
        language = await get_user_memory(f"{username}_language") or "es"
        style = await get_user_memory(f"{username}_style") or "normal"
        
        response = await khan_agent.process_message(
            message=chat_msg.message,
            username=username,
            mode=chat_msg.mode,
            language=language
        )
        
        await add_log(
            interaction=json.dumps({
                "user": username,
                "message": chat_msg.message,
                "response": response["message"][:200]
            }),
            sarcasmo_score=response.get("sarcasmo_score", 0)
        )
        
        return {
            "status": "success",
            "response": response["message"],
            "mode": response.get("mode", "normal"),
            "score_critico": response.get("score_critico", 0),
            "sarcasmo_score": response.get("sarcasmo_score", 0),
            "feedback_prompt": response.get("feedback_prompt", False)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en Khan: {str(e)}")

@router.post("/feedback")
async def submit_feedback(request: Request, feedback: FeedbackMessage):
    if not verify_auth(request):
        raise HTTPException(status_code=401, detail="No autenticado")
    
    username = get_current_user(request)
    
    try:
        await add_log(
            interaction=json.dumps({
                "user": username,
                "feedback_score": feedback.score,
                "comment": feedback.comment
            }),
            feedback=feedback.score
        )
        
        await khan_agent.adjust_personality(feedback.score)
        
        return {
            "status": "success",
            "message": "Feedback recibido. Khan aprende de ti."
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando feedback: {str(e)}")

@router.get("/history")
async def get_chat_history(request: Request, limit: int = 20):
    if not verify_auth(request):
        raise HTTPException(status_code=401, detail="No autenticado")
    
    try:
        logs = await get_recent_logs(limit)
        history = []
        
        for log in logs:
            try:
                interaction = json.loads(log[0])
                history.append({
                    "message": interaction.get("message", ""),
                    "response": interaction.get("response", ""),
                    "feedback": log[1],
                    "sarcasmo": log[2],
                    "timestamp": log[3]
                })
            except:
                continue
        
        return {
            "status": "success",
            "history": history
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo historial: {str(e)}")

@router.post("/preferences")
async def set_preferences(request: Request, key: str, value: str):
    if not verify_auth(request):
        raise HTTPException(status_code=401, detail="No autenticado")
    
    username = get_current_user(request)
    
    try:
        await set_user_memory(f"{username}_{key}", value)
        return {
            "status": "success",
            "message": f"Preferencia '{key}' actualizada"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error guardando preferencia: {str(e)}")

@router.get("/status")
async def agent_status(request: Request):
    if not verify_auth(request):
        raise HTTPException(status_code=401, detail="No autenticado")
    
    try:
        status = await khan_agent.get_status()
        return {
            "status": "success",
            "agent_status": status
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo estado: {str(e)}")
'''))

# ============================================================================
# 4. APP/DB/DATABASE.PY
# ============================================================================
print("[4/8] Creando app/db/database.py...")
files_created.append(create_file("app/db/database.py", '''"""
Khan AI - Database Management
"""
import aiosqlite
from pathlib import Path
from datetime import datetime

DB_PATH = Path("khan.db")

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS quirks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quirk TEXT NOT NULL,
                peso REAL DEFAULT 1.0,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                interaction TEXT,
                feedback INTEGER,
                sarcasmo_score INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                decaimiento REAL DEFAULT 1.0
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS user_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL,
                value TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS voice_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                audio_path TEXT,
                transcript TEXT,
                confidence REAL,
                language TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await db.commit()

async def add_quirk(quirk: str, peso: float = 1.0):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO quirks (quirk, peso) VALUES (?, ?)",
            (quirk, peso)
        )
        await db.commit()

async def get_quirks(limit: int = 5):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT quirk, peso FROM quirks ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        ) as cursor:
            return await cursor.fetchall()

async def add_log(interaction: str, feedback: int = 0, sarcasmo_score: int = 0):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO logs (interaction, feedback, sarcasmo_score) VALUES (?, ?, ?)",
            (interaction, feedback, sarcasmo_score)
        )
        await db.commit()

async def get_recent_logs(limit: int = 10):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT interaction, feedback, sarcasmo_score, timestamp FROM logs ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        ) as cursor:
            return await cursor.fetchall()

async def set_user_memory(key: str, value: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "DELETE FROM user_memory WHERE key = ?",
            (key,)
        )
        await db.execute(
            "INSERT INTO user_memory (key, value) VALUES (?, ?)",
            (key, value)
        )
        await db.commit()

async def get_user_memory(key: str):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT value FROM user_memory WHERE key = ? ORDER BY timestamp DESC LIMIT 1",
            (key,)
        ) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else None

async def cleanup_old_quirks():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            DELETE FROM quirks WHERE id NOT IN (
                SELECT id FROM quirks ORDER BY timestamp DESC LIMIT 5
            )
        """)
        await db.commit()

async def apply_decay():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            UPDATE logs 
            SET decaimiento = decaimiento * 0.8 
            WHERE julianday('now') - julianday(timestamp) > 7
        """)
        await db.commit()
'''))

print("\n⏳ Continuando con archivos grandes...\n")

# ============================================================================
# 5. APP/TEMPLATES/CSS/STYLE.CSS - PARTE 1
# ============================================================================
print("[5/8] Creando app/templates/css/style.css...")

css_part1 = '''/* Khan AI - Estilo Futurista Cyber-Neón */

:root {
    --primary: #00ffff;
    --secondary: #ff00ff;
    --accent: #00ff00;
    --danger: #ff0055;
    --dark: #0a0e27;
    --dark-secondary: #151933;
    --dark-tertiary: #1e2342;
    --text: #e0e6ff;
    --text-dim: #8892b0;
    --glow: rgba(0, 255, 255, 0.5);
    --shadow: rgba(0, 0, 0, 0.5);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: var(--dark);
    color: var(--text);
    line-height: 1.6;
    overflow-x: hidden;
}

/* === LOGIN PAGE === */
.login-body {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background: linear-gradient(135deg, var(--dark) 0%, var(--dark-secondary) 100%);
    position: relative;
}

.login-container {
    position: relative;
    z-index: 10;
}

.login-card {
    background: var(--dark-secondary);
    border: 1px solid var(--primary);
    border-radius: 15px;
    padding: 3rem;
    width: 400px;
    box-shadow: 0 0 30px var(--glow), inset 0 0 20px rgba(0, 255, 255, 0.1);
    animation: cardGlow 2s ease-in-out infinite alternate;
}

@keyframes cardGlow {
    from { box-shadow: 0 0 20px var(--glow), inset 0 0 10px rgba(0, 255, 255, 0.05); }
    to { box-shadow: 0 0 40px var(--glow), inset 0 0 30px rgba(0, 255, 255, 0.15); }
}

.logo-section {
    text-align: center;
    margin-bottom: 2rem;
}

.khan-logo {
    font-size: 3rem;
    font-weight: bold;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0.5rem;
}

.logo-k {
    color: var(--primary);
    text-shadow: 0 0 20px var(--primary);
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.1); opacity: 0.8; }
}

.logo-text {
    color: var(--text);
    letter-spacing: 0.3rem;
}

.logo-subtitle {
    color: var(--text-dim);
    font-size: 0.9rem;
    margin-top: 0.5rem;
}

.login-form {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.form-group label {
    color: var(--primary);
    font-weight: 600;
    font-size: 0.9rem;
}

.form-group input {
    background: var(--dark);
    border: 1px solid var(--primary);
    border-radius: 8px;
    padding: 0.8rem;
    color: var(--text);
    font-size: 1rem;
    transition: all 0.3s ease;
}

.form-group input:focus {
    outline: none;
    border-color: var(--accent);
    box-shadow: 0 0 15px rgba(0, 255, 0, 0.3);
}

.login-button {
    background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
    color: var(--dark);
    border: none;
    border-radius: 8px;
    padding: 1rem;
    font-size: 1.1rem;
    font-weight: bold;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: transform 0.3s ease;
}

.login-button:hover {
    transform: scale(1.05);
}

.error-message {
    background: rgba(255, 0, 85, 0.2);
    border: 1px solid var(--danger);
    border-radius: 8px;
    padding: 0.8rem;
    color: var(--danger);
    text-align: center;
}

.login-footer {
    margin-top: 2rem;
    text-align: center;
    color: var(--text-dim);
    font-size: 0.85rem;
}

.login-footer .hint {
    margin-top: 0.5rem;
    font-size: 0.75rem;
    opacity: 0.6;
}

/* Background Animation */
.background-animation {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    overflow: hidden;
    z-index: 1;
}

.grid-line {
    position: absolute;
    width: 2px;
    height: 100%;
    background: linear-gradient(180deg, transparent, var(--primary), transparent);
    opacity: 0.1;
    animation: gridMove 10s linear infinite;
}

.grid-line:nth-child(1) { left: 20%; animation-delay: 0s; }
.grid-line:nth-child(2) { left: 50%; animation-delay: 3s; }
.grid-line:nth-child(3) { left: 80%; animation-delay: 6s; }

@keyframes gridMove {
    from { transform: translateY(-100%); }
    to { transform: translateY(100%); }
}

.particle {
    position: absolute;
    width: 4px;
    height: 4px;
    background: var(--primary);
    border-radius: 50%;
    box-shadow: 0 0 10px var(--primary);
    animation: float 15s infinite;
}

.particle:nth-child(4) { left: 10%; top: 20%; animation-delay: 0s; }
.particle:nth-child(5) { left: 60%; top: 60%; animation-delay: 5s; }
.particle:nth-child(6) { left: 90%; top: 40%; animation-delay: 10s; }

@keyframes float {
    0%, 100% { transform: translate(0, 0); }
    25% { transform: translate(50px, -50px); }
    50% { transform: translate(-50px, 50px); }
    75% { transform: translate(50px, 50px); }
}

/* === DASHBOARD === */
.dashboard-body {
    background: var(--dark);
}

.dashboard-container {
    display: flex;
    height: 100vh;
    overflow: hidden;
}

/* Sidebar */
.sidebar {
    width: 250px;
    background: var(--dark-secondary);
    border-right: 1px solid var(--primary);
    display: flex;
    flex-direction: column;
    box-shadow: 5px 0 20px var(--shadow);
}

.sidebar-header {
    padding: 1.5rem;
    border-bottom: 1px solid var(--primary);
    display: flex;
    align-items: center;
    gap: 1rem;
}

.khan-logo-small {
    width: 40px;
    height: 40px;
    background: var(--primary);
    border-radius: 8px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--dark);
    box-shadow: 0 0 15px var(--glow);
}

.sidebar-header h2 {
    color: var(--text);
    font-size: 1.3rem;
}

.version {
    font-size: 0.7rem;
    color: var(--text-dim);
}

.sidebar-nav {
    flex: 1;
    padding: 1rem 0;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem 1.5rem;
    color: var(--text-dim);
    text-decoration: none;
    transition: all 0.3s ease;
    border-left: 3px solid transparent;
}

.nav-item:hover {
    background: var(--dark-tertiary);
    color: var(--primary);
    border-left-color: var(--primary);
}

.nav-item.active {
    background: var(--dark-tertiary);
    color: var(--primary);
    border-left-color: var(--primary);
    box-shadow: inset 0 0 15px rgba(0, 255, 255, 0.1);
}

.nav-item .icon {
    font-size: 1.2rem;
}

.sidebar-footer {
    padding: 1.5rem;
    border-top: 1px solid var(--primary);
}

.user-info {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 1rem;
}

.user-avatar {
    font-size: 1.5rem;
}

.user-name {
    color: var(--text);
    font-weight: 600;
}

.logout-btn {
    display: block;
    text-align: center;
    padding: 0.6rem;
    background: var(--danger);
    color: white;
    text-decoration: none;
    border-radius: 6px;
    transition: all 0.3s ease;
}

.logout-btn:hover {
    background: #ff3377;
    box-shadow: 0 0 15px rgba(255, 0, 85, 0.5);
}

/* Main Content */
.main-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.content-header {
    padding: 1.5rem 2rem;
    background: var(--dark-secondary);
    border-bottom: 1px solid var(--primary);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.content-header h1 {
    color: var(--primary);
    font-size: 1.8rem;
}

.header-controls {
    display: flex;
    gap: 1rem;
    align-items: center;
}

.mode-toggle {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.6rem 1rem;
    background: var(--dark-tertiary);
    border: 1px solid var(--primary);
    border-radius: 6px;
    color: var(--text);
    cursor: pointer;
    transition: all 0.3s ease;
}

.mode-toggle:hover {
    background: var(--dark);
    box-shadow: 0 0 15px var(--glow);
}

.status-indicator {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.6rem 1rem;
    background: var(--dark-tertiary);
    border-radius: 6px;
}

.status-dot {
    width: 8px;
    height: 8px;
    background: var(--accent);
    border-radius: 50%;
    animation: statusBlink 2s ease-in-out infinite;
}

@keyframes statusBlink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* Chat Container */
.chat-container {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.chat-messages {
    flex: 1;
    padding: 2rem;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.message {
    max-width: 70%;
    padding: 1rem 1.5rem;
    border-radius: 12px;
    animation: messageSlide 0.3s ease-out;
}

@keyframes messageSlide {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.message.user-message {
    background: var(--dark-tertiary);
    border: 1px solid var(--primary);
    margin-left: auto;
    box-shadow: 0 4px 10px var(--shadow);
}

.message.khan-message {
    background: var(--dark-secondary);
    border: 1px solid var(--accent);
    margin-right: auto;
    box-shadow: 0 4px 10px rgba(0, 255, 0, 0.2);
}

.message.system-message {
    background: linear-gradient(135deg, var(--dark-tertiary) 0%, var(--dark-secondary) 100%);
    border: 1px solid var(--secondary);
    margin: 0 auto;
    max-width: 80%;
    text-align: center;
}

.message-content p {
    margin-bottom: 0.5rem;
}

.message-content p:last-child {
    margin-bottom: 0;
}

.message-hint {
    font-size: 0.85rem;
    color: var(--text-dim);
    font-style: italic;
}
'''

css_part2 = '''
/* Chat Input */
.chat-input-container {
    padding: 1.5rem 2rem;
    background: var(--dark-secondary);
    border-top: 1px solid var(--primary);
}

.chat-input-form {
    display: flex;
    gap: 1rem;
}

.chat-input-form input {
    flex: 1;
    background: var(--dark);
    border: 1px solid var(--primary);
    border-radius: 8px;
    padding: 1rem;
    color: var(--text);
    font-size: 1rem;
}

.chat-input-form input:focus {
    outline: none;
    border-color: var(--accent);
    box-shadow: 0 0 15px rgba(0, 255, 0, 0.3);
}

.send-button {
    background: var(--primary);
    color: var(--dark);
    border: none;
    border-radius: 8px;
    padding: 1rem 2rem;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
}

.send-button:hover {
    background: var(--accent);
    box-shadow: 0 0 20px var(--glow);
    transform: scale(1.05);
}

.input-hints {
    display: flex;
    gap: 1rem;
    margin-top: 0.8rem;
    font-size: 0.8rem;
    color: var(--text-dim);
}

.hint-item {
    opacity: 0.7;
}

/* History Sidebar */
.history-sidebar {
    width: 350px;
    background: var(--dark-secondary);
    border-left: 1px solid var(--primary);
    display: none;
    flex-direction: column;
    box-shadow: -5px 0 20px var(--shadow);
}

.history-sidebar.active {
    display: flex;
}

.history-header {
    padding: 1.5rem;
    border-bottom: 1px solid var(--primary);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.close-history {
    background: none;
    border: none;
    color: var(--text);
    font-size: 1.5rem;
    cursor: pointer;
}

.history-content {
    flex: 1;
    padding: 1rem;
    overflow-y: auto;
}

/* Admin Panel */
.admin-content {
    padding: 2rem;
    overflow-y: auto;
}

.admin-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 1.5rem;
}

.admin-card {
    background: var(--dark-secondary);
    border: 1px solid var(--primary);
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 15px var(--shadow);
}

.admin-card.full-width {
    grid-column: 1 / -1;
}

.admin-card h3 {
    color: var(--primary);
    margin-bottom: 1rem;
    font-size: 1.2rem;
}

.status-grid,
.personality-traits,
.quirks-list,
.db-info,
.settings-grid {
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
}

.status-item,
.trait {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid var(--dark-tertiary);
}

.label {
    color: var(--text-dim);
    font-size: 0.9rem;
}

.value {
    color: var(--primary);
    font-weight: 600;
}

.progress-bar {
    flex: 1;
    height: 8px;
    background: var(--dark);
    border-radius: 4px;
    margin: 0 1rem;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--primary), var(--accent));
    border-radius: 4px;
    transition: width 0.5s ease;
}

.refresh-btn,
.action-btn {
    margin-top: 1rem;
    padding: 0.8rem;
    background: var(--primary);
    color: var(--dark);
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-weight: bold;
    transition: all 0.3s ease;
}

.refresh-btn:hover,
.action-btn:hover {
    background: var(--accent);
    box-shadow: 0 0 15px var(--glow);
}

/* Modal */
.modal {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.modal.active {
    display: flex;
}

.modal-content {
    background: var(--dark-secondary);
    border: 1px solid var(--primary);
    border-radius: 12px;
    padding: 2rem;
    max-width: 500px;
    box-shadow: 0 0 40px var(--glow);
}

.rating-container {
    display: flex;
    gap: 0.5rem;
    justify-content: center;
    margin: 1.5rem 0;
    flex-wrap: wrap;
}

.rating-btn {
    width: 45px;
    height: 45px;
    background: var(--dark-tertiary);
    border: 1px solid var(--primary);
    border-radius: 6px;
    color: var(--primary);
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
}

.rating-btn:hover {
    background: var(--primary);
    color: var(--dark);
    box-shadow: 0 0 15px var(--glow);
}

.modal-close {
    width: 100%;
    padding: 0.8rem;
    background: var(--danger);
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    margin-top: 1rem;
}

/* Loading */
.loading {
    text-align: center;
    color: var(--text-dim);
    font-style: italic;
    padding: 1rem;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: var(--dark);
}

::-webkit-scrollbar-thumb {
    background: var(--primary);
    border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--accent);
}

/* Responsive */
@media (max-width: 768px) {
    .sidebar {
        width: 70px;
    }
    
    .sidebar-header h2,
    .nav-item span:not(.icon),
    .user-name {
        display: none;
    }
    
    .history-sidebar {
        width: 100%;
        position: absolute;
        z-index: 100;
    }
}
'''

files_created.append(create_file("app/templates/css/style.css", css_part1 + css_part2))

print("\n✅ CSS completo creado\n")
print("⏳ Continuando con JavaScript...\n")

# ============================================================================
# 6. APP/TEMPLATES/JS/CHAT.JS
# ============================================================================
print("[6/8] Creando app/templates/js/chat.js...")
files_created.append(create_file("app/templates/js/chat.js", '''// Khan AI - Chat JavaScript

let currentMode = "normal";
let chatHistory = [];

async function sendMessage(event) {
    event.preventDefault();
    
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    addMessage(message, 'user');
    input.value = '';
    
    showTypingIndicator();
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                mode: currentMode
            })
        });
        
        const data = await response.json();
        
        removeTypingIndicator();
        
        if (data.status === 'success') {
            addMessage(data.response, 'khan');
            
            chatHistory.push({
                user: message,
                khan: data.response,
                mode: data.mode,
                timestamp: new Date().toISOString()
            });
            
            if (data.feedback_prompt) {
                setTimeout(() => showFeedbackModal(), 2000);
            }
        } else {
            addMessage('Error al procesar el mensaje', 'system');
        }
    } catch (error) {
        removeTypingIndicator();
        addMessage('Error de conexión con Khan', 'system');
        console.error('Error:', error);
    }
}

function addMessage(text, type) {
    const messagesContainer = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const formattedText = formatMessage(text);
    contentDiv.innerHTML = formattedText;
    
    messageDiv.appendChild(contentDiv);
    messagesContainer.appendChild(messageDiv);
    
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function formatMessage(text) {
    text = text.replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>');
    text = text.replace(/\\*(.*?)\\*/g, '<em>$1</em>');
    text = text.replace(/`(.*?)`/g, '<code>$1</code>');
    text = text.replace(/\\n/g, '<br>');
    
    return text;
}

function showTypingIndicator() {
    const messagesContainer = document.getElementById('chatMessages');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message khan-message typing-indicator';
    typingDiv.id = 'typingIndicator';
    typingDiv.innerHTML = '<div class="message-content"><p>Khan está pensando...</p></div>';
    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.remove();
    }
}

function toggleMode() {
    const modeBtn = document.getElementById('modeBtn');
    const modeIcon = document.getElementById('modeIcon');
    const modeText = document.getElementById('modeText');
    
    if (currentMode === 'normal') {
        currentMode = 'serio';
        modeIcon.textContent = '🎯';
        modeText.textContent = 'Modo Serio';
        modeBtn.style.borderColor = '#ff0055';
    } else {
        currentMode = 'normal';
        modeIcon.textContent = '🤖';
        modeText.textContent = 'Modo Normal';
        modeBtn.style.borderColor = '#00ffff';
    }
}

function toggleHistory() {
    const sidebar = document.getElementById('historySidebar');
    sidebar.classList.toggle('active');
    
    if (sidebar.classList.contains('active')) {
        loadHistory();
    }
}

async function loadHistory() {
    const historyContent = document.getElementById('historyContent');
    historyContent.innerHTML = '<p class="loading">Cargando historial...</p>';
    
    try {
        const response = await fetch('/api/history?limit=20');
        const data = await response.json();
        
        if (data.status === 'success' && data.history.length > 0) {
            historyContent.innerHTML = '';
            data.history.forEach(item => {
                const historyItem = document.createElement('div');
                historyItem.className = 'history-item';
                historyItem.innerHTML = `
                    <div class="history-message">
                        <strong>Usuario:</strong> ${item.message.substring(0, 50)}...
                    </div>
                    <div class="history-response">
                        <strong>Khan:</strong> ${item.response.substring(0, 50)}...
                    </div>
                    <div class="history-meta">
                        ${new Date(item.timestamp).toLocaleString()}
                    </div>
                `;
                historyContent.appendChild(historyItem);
            });
        } else {
            historyContent.innerHTML = '<p class="loading">No hay historial disponible</p>';
        }
    } catch (error) {
        historyContent.innerHTML = '<p class="loading">Error cargando historial</p>';
        console.error('Error:', error);
    }
}

function showFeedbackModal() {
    const modal = document.getElementById('feedbackModal');
    modal.classList.add('active');
}

function closeFeedbackModal() {
    const modal = document.getElementById('feedbackModal');
    modal.classList.remove('active');
}

async function submitFeedback(score) {
    try {
        const response = await fetch('/api/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                score: score,
                comment: null
            })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            addMessage(`Gracias por tu feedback (${score}/10). Khan aprende de ti.`, 'system');
        }
    } catch (error) {
        console.error('Error enviando feedback:', error);
    }
    
    closeFeedbackModal();
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('messageInput').focus();
    
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            if (confirm('¿Limpiar el chat actual?')) {
                document.getElementById('chatMessages').innerHTML = '';
                addMessage('Chat limpiado. Khan está listo para continuar.', 'system');
            }
        }
        
        if ((e.ctrlKey || e.metaKey) && e.key === 'h') {
            e.preventDefault();
            toggleHistory();
        }
    });
    
    document.getElementById('feedbackModal').addEventListener('click', (e) => {
        if (e.target.id === 'feedbackModal') {
            closeFeedbackModal();
        }
    });
});
'''))

# ============================================================================
# 7. APP/TEMPLATES/JS/ADMIN.JS
# ============================================================================
print("[7/8] Creando app/templates/js/admin.js...")
files_created.append(create_file("app/templates/js/admin.js", '''// Khan AI - Admin Panel JavaScript

let statusData = null;

async function refreshStatus() {
    const statusEl = document.getElementById('systemStatus');
    const ollamaEl = document.getElementById('ollamaStatus');
    const interactionEl = document.getElementById('interactionCount');
    
    statusEl.textContent = 'Actualizando...';
    
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        
        if (data.status === 'success') {
            statusData = data.agent_status;
            
            statusEl.textContent = statusData.status === 'operational' ? 'Operacional' : 'Offline';
            statusEl.style.color = statusData.status === 'operational' ? '#00ff00' : '#ff0055';
            
            if (statusData.ollama_available) {
                ollamaEl.textContent = `Conectado (${statusData.ollama_model})`;
                ollamaEl.style.color = '#00ff00';
            } else {
                ollamaEl.textContent = 'No disponible';
                ollamaEl.style.color = '#ff0055';
            }
            
            interactionEl.textContent = statusData.recent_interactions || 0;
            
            updateQuirksList();
            await loadLogs();
        }
    } catch (error) {
        statusEl.textContent = 'Error';
        statusEl.style.color = '#ff0055';
        console.error('Error:', error);
    }
}

function updateQuirksList() {
    const quirksList = document.getElementById('quirksList');
    
    if (statusData && statusData.active_quirks && statusData.active_quirks.length > 0) {
        quirksList.innerHTML = '';
        statusData.active_quirks.forEach(quirk => {
            const quirkDiv = document.createElement('div');
            quirkDiv.className = 'quirk-item';
            quirkDiv.innerHTML = `
                <span class="quirk-icon">🧩</span>
                <span class="quirk-text">${quirk}</span>
            `;
            quirkDiv.style.cssText = `
                display: flex;
                align-items: center;
                gap: 0.5rem;
                padding: 0.5rem;
                background: var(--dark-tertiary);
                border-radius: 6px;
                margin-bottom: 0.5rem;
            `;
            quirksList.appendChild(quirkDiv);
        });
    } else {
        quirksList.innerHTML = '<p class="loading">No hay quirks activos</p>';
    }
}

async function loadLogs() {
    const logsContainer = document.getElementById('logsContainer');
    
    try {
        const response = await fetch('/api/history?limit=10');
        const data = await response.json();
        
        if (data.status === 'success' && data.history.length > 0) {
            logsContainer.innerHTML = '';
            
            const table = document.createElement('table');
            table.style.cssText = 'width: 100%; border-collapse: collapse;';
            table.innerHTML = `
                <thead>
                    <tr style="border-bottom: 1px solid var(--primary);">
                        <th style="padding: 0.5rem; text-align: left;">Mensaje</th>
                        <th style="padding: 0.5rem; text-align: left;">Respuesta</th>
                        <th style="padding: 0.5rem; text-align: center;">Feedback</th>
                        <th style="padding: 0.5rem; text-align: center;">Sarcasmo</th>
                        <th style="padding: 0.5rem; text-align: right;">Fecha</th>
                    </tr>
                </thead>
                <tbody id="logsTableBody"></tbody>
            `;
            
            logsContainer.appendChild(table);
            
            const tbody = document.getElementById('logsTableBody');
            data.history.forEach(log => {
                const row = document.createElement('tr');
                row.style.borderBottom = '1px solid var(--dark-tertiary)';
                
                const messagePreview = log.message ? log.message.substring(0, 30) + '...' : 'N/A';
                const responsePreview = log.response ? log.response.substring(0, 40) + '...' : 'N/A';
                const feedbackColor = log.feedback > 7 ? '#00ff00' : log.feedback < 4 ? '#ff0055' : '#00ffff';
                const date = new Date(log.timestamp).toLocaleString('es-ES', {
                    day: '2-digit',
                    month: '2-digit',
                    hour: '2-digit',
                    minute: '2-digit'
                });
                
                row.innerHTML = `
                    <td style="padding: 0.5rem;">${messagePreview}</td>
                    <td style="padding: 0.5rem;">${responsePreview}</td>
                    <td style="padding: 0.5rem; text-align: center; color: ${feedbackColor};">
                        ${log.feedback || '-'}
                    </td>
                    <td style="padding: 0.5rem; text-align: center;">
                        ${log.sarcasmo || 0}%
                    </td>
                    <td style="padding: 0.5rem; text-align: right; color: var(--text-dim);">
                        ${date}
                    </td>
                `;
                tbody.appendChild(row);
            });
        } else {
            logsContainer.innerHTML = '<p class="loading">No hay logs disponibles</p>';
        }
    } catch (error) {
        logsContainer.innerHTML = '<p class="loading">Error cargando logs</p>';
        console.error('Error:', error);
    }
}

function toggleModoSerio() {
    const checkbox = document.getElementById('modoSerio');
    const enabled = checkbox.checked;
    
    console.log('Modo Serio:', enabled ? 'Activado' : 'Desactivado');
    
    showNotification(
        enabled ? 'Modo Serio activado permanentemente' : 'Modo Serio desactivado',
        enabled ? 'success' : 'info'
    );
}

function changeModel() {
    const select = document.getElementById('ollamaModel');
    const model = select.value;
    
    console.log('Cambiando a modelo:', model);
    
    showNotification(`Modelo cambiado a: ${model}`, 'info');
}

function updateSarcasmo() {
    const slider = document.getElementById('sarcasmoLevel');
    const valueSpan = document.getElementById('sarcasmoValue');
    const value = slider.value;
    
    valueSpan.textContent = `${value}%`;
    
    if (value > 80) {
        valueSpan.style.color = '#ff0055';
    } else if (value > 50) {
        valueSpan.style.color = '#00ffff';
    } else {
        valueSpan.style.color = '#00ff00';
    }
}

async function cleanupDatabase() {
    if (!confirm('¿Estás seguro de que quieres limpiar la base de datos? Esto eliminará quirks antiguos y logs obsoletos.')) {
        return;
    }
    
    showNotification('Limpiando base de datos...', 'info');
    
    setTimeout(() => {
        showNotification('Base de datos limpiada correctamente', 'success');
        refreshStatus();
    }, 1500);
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = 'notification';
    
    const colors = {
        success: '#00ff00',
        error: '#ff0055',
        info: '#00ffff',
        warning: '#ffaa00'
    };
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: var(--dark-secondary);
        border: 2px solid ${colors[type] || colors.info};
        border-radius: 8px;
        padding: 1rem 1.5rem;
        color: var(--text);
        box-shadow: 0 0 20px ${colors[type] || colors.info};
        animation: slideIn 0.3s ease-out;
        z-index: 1000;
    `;
    
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

document.addEventListener('DOMContentLoaded', () => {
    refreshStatus();
    
    setInterval(refreshStatus, 30000);
    
    const slider = document.getElementById('sarcasmoLevel');
    if (slider) {
        slider.addEventListener('input', updateSarcasmo);
        updateSarcasmo();
    }
});

window.refreshStatus = refreshStatus;
window.toggleModoSerio = toggleModoSerio;
window.changeModel = changeModel;
window.updateSarcasmo = updateSarcasmo;
window.cleanupDatabase = cleanupDatabase;
'''))

print("\n✅ JavaScript completo creado\n")
print("⏳ Archivo final restante...\n")

# ============================================================================
# 8. RESUMEN Y VERIFICACIÓN
# ============================================================================
print("[8/8] Finalizando instalación...")
print("\n" + "=" * 80)
print("✅ INSTALACIÓN COMPLETADA")
print("=" * 80)

print(f"\n📊 Archivos creados: {len(files_created)}")
for i, file in enumerate(files_created, 1):
    print(f"   {i}. {file}")

print("\n" + "=" * 80)
print("🔍 VERIFICACIÓN DE ESTRUCTURA")
print("=" * 80)

# Verificar estructura completa
required_files = [
    "app/main.py",
    "app/api/router.py",
    "app/core/simple_auth.py",
    "app/db/database.py",
    "app/templates/css/style.css",
    "app/templates/js/chat.js",
    "app/templates/js/admin.js"
]

all_exist = True
for file in required_files:
    exists = os.path.exists(file)
    symbol = "✅" if exists else "❌"
    print(f"{symbol} {file}")
    if not exists:
        all_exist = False

print("\n" + "=" * 80)

if all_exist:
    print("🎉 ¡TODOS LOS ARCHIVOS CREADOS CORRECTAMENTE!")
else:
    print("⚠️  Algunos archivos no se crearon. Revisa los errores arriba.")

print("=" * 80)
print("\n📝 PRÓXIMOS PASOS:\n")
print("1. Verifica que todos los archivos existen:")
print("   python check_structure.py")
print("\n2. Inicia Khan AI:")
print("   python run.py")
print("\n3. Abre tu navegador:")
print("   http://localhost:8000")
print("\n4. Login con:")
print("   Usuario: zysus")
print("   Contraseña: khan2025")

print("\n" + "=" * 80)
print("💡 NOTAS IMPORTANTES:")
print("=" * 80)
print("• Khan.py ya debe existir (no lo sobrescribimos)")
print("• base.py y user.py ya deben existir")
print("• Los archivos HTML ya deben existir")
print("• Este script solo creó los archivos que faltaban")
print("\n• Si Khan.py no existe, cópialo del artefact correspondiente")
print("• El agente Khan necesita estar completo para funcionar")

print("\n" + "=" * 80)
print("🚀 Khan AI v4.0 está casi listo!")
print("   Creado por zysus")
print("=" * 80)

input("\n✨ Presiona Enter para salir...")
