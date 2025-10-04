"""
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
