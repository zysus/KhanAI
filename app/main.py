"""
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
