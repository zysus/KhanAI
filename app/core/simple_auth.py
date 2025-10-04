"""
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
