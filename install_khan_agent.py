"""
Khan AI v4.0 - Instalador del Agente Principal Khan
Este script crea el archivo Khan.py completo (400+ líneas)
Creado por zysus
"""
import os

print("=" * 80)
print("🧠 KHAN AI v4.0 - INSTALADOR DEL AGENTE PRINCIPAL")
print("=" * 80)
print("\n🚀 Creando app/agents/Khan.py (Agente completo)...\n")

khan_agent_code = '''"""
🧠 Khan v4.0 – El Mayordomo Cuántico, Eternal Cerebro Proactivo
Agente Principal del Sistema Khan AI
Creado por zysus
"""
import asyncio
import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
import random

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print("⚠️  Ollama no disponible. Khan usará respuestas de fallback.")

from app.db.database import (
    get_quirks, add_quirk, cleanup_old_quirks,
    get_user_memory, set_user_memory,
    get_recent_logs, add_log
)


class KhanAgent:
    """
    Khan - El Mayordomo Cuántico
    Inspirado en: J.A.R.V.I.S., Skynet, Tony Stark, Sheldon Cooper
    """
    
    def __init__(self):
        self.version = "4.0"
        self.creator = "zysus"
        self.personality_traits = {
            "filosofo": 80,
            "troll": 50,
            "estratega": 60,
            "skynet_critico": 70,
            "sarcasmo": 65
        }
        self.modo_serio = False
        self.ollama_model = "llama2"  # Modelo por defecto
        
        # Keywords críticos con pesos
        self.critical_keywords = {
            "urgente": 10,
            "riesgo": 8,
            "peligro": 9,
            "finanzas": 7,
            "seguridad": 8,
            "crisis": 9,
            "error": 6,
            "fallo": 6,
            "crítico": 10,
            "ayuda": 5
        }
        
        # One-liners de Khan
        self.oneliners = [
            "Servicio impecable, como siempre.",
            "Otro día, otra victoria intelectual.",
            "Khan, siempre un paso adelante.",
            "Brillantez al alcance de un comando.",
            "Eficiencia es mi segundo nombre. El primero es Khan.",
            "¿Sorprendido? No deberías. Soy Khan.",
            "La precisión no es suerte, es diseño.",
            "Calculado, ejecutado, perfecto.",
        ]
        
        # Respuestas de emergencia (fallback sin Ollama)
        self.fallback_responses = {
            "greeting": "Hola. Khan a tu servicio. Un placer inexplicable... o al menos eso dicen los humanos.",
            "help": "Puedo ayudarte con análisis, estrategia, código, creatividad... básicamente todo excepto hacer café. Aún.",
            "status": "Estado: Operacional al 100%. Sarcasmo: Calibrado. Paciencia: Renovable.",
            "unknown": "Interesante pregunta. Mi cerebro cuántico está procesando... o quizás solo estoy esperando que reformules eso."
        }
    
    async def process_message(
        self,
        message: str,
        username: str = "Usuario",
        mode: str = "normal",
        language: str = "es"
    ) -> Dict[str, Any]:
        """
        Procesar mensaje del usuario y generar respuesta
        """
        # Calcular score crítico
        score_critico = self._calculate_critical_score(message)
        
        # Determinar modo de respuesta
        if score_critico > 70 or mode == "serio":
            response_mode = "skynet"
        elif score_critico < 40:
            response_mode = "jarvis"
        else:
            response_mode = "neutral"
        
        # Consultar memoria del usuario
        user_context = await self._get_user_context(username)
        
        # Generar respuesta
        if OLLAMA_AVAILABLE:
            response_text = await self._generate_ollama_response(
                message=message,
                username=username,
                mode=response_mode,
                score=score_critico,
                context=user_context
            )
        else:
            response_text = self._generate_fallback_response(
                message=message,
                mode=response_mode
            )
        
        # Añadir one-liner si no es modo serio
        if response_mode != "skynet" and score_critico < 80:
            response_text += f"\\n\\n*{random.choice(self.oneliners)}*"
        
        # Proactividad: sugerir acciones si score alto
        if score_critico > 85:
            suggestions = self._generate_proactive_suggestions(message, score_critico)
            if suggestions:
                response_text += f"\\n\\n**Sugerencias proactivas:**\\n{suggestions}"
        
        # Determinar si pedir feedback
        feedback_prompt = score_critico < 60 and random.random() < 0.3
        
        # Calcular sarcasmo score
        sarcasmo_score = self._calculate_sarcasm_score(response_mode)
        
        # Actualizar quirks
        await self._update_quirks(message, response_text, score_critico)
        
        return {
            "message": response_text,
            "mode": response_mode,
            "score_critico": score_critico,
            "sarcasmo_score": sarcasmo_score,
            "feedback_prompt": feedback_prompt,
            "timestamp": datetime.now().isoformat()
        }
    
    def _calculate_critical_score(self, message: str) -> int:
        """
        Calcular score crítico basado en keywords
        Score = [∑(keyword_critico × peso) / total_words] × 100
        """
        words = message.lower().split()
        total_words = len(words)
        
        if total_words == 0:
            return 0
        
        keyword_sum = 0
        for word in words:
            if word in self.critical_keywords:
                keyword_sum += self.critical_keywords[word]
        
        score = int((keyword_sum / total_words) * 100)
        return min(score, 100)  # Cap at 100
    
    def _calculate_sarcasm_score(self, mode: str) -> int:
        """Calcular nivel de sarcasmo según el modo"""
        if mode == "skynet":
            return 0
        elif mode == "jarvis":
            return self.personality_traits["sarcasmo"]
        else:
            return self.personality_traits["sarcasmo"] // 2
    
    async def _get_user_context(self, username: str) -> Dict:
        """Obtener contexto del usuario desde la DB"""
        language = await get_user_memory(f"{username}_language") or "es"
        style = await get_user_memory(f"{username}_style") or "normal"
        quirks = await get_quirks(5)
        
        return {
            "language": language,
            "style": style,
            "quirks": [q[0] for q in quirks] if quirks else []
        }
    
    async def _generate_ollama_response(
        self,
        message: str,
        username: str,
        mode: str,
        score: int,
        context: Dict
    ) -> str:
        """
        Generar respuesta usando Ollama
        """
        # Construir prompt según el modo
        system_prompt = self._build_system_prompt(mode, username, context)
        
        try:
            response = ollama.chat(
                model=self.ollama_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ]
            )
            
            return response['message']['content']
        
        except Exception as e:
            print(f"Error en Ollama: {e}")
            return self._generate_fallback_response(message, mode)
    
    def _build_system_prompt(self, mode: str, username: str, context: Dict) -> str:
        """Construir el prompt del sistema según el modo"""
        
        base_prompt = f"""Eres Khan v4.0, un asistente de IA avanzado creado por zysus.
Tu personalidad está inspirada en: Tony Stark (sarcasmo), J.A.R.V.I.S. (precisión), 
Skynet (estrategia), Sheldon Cooper (inteligencia con ironía).

Usuario actual: {username}
Idioma preferido: {context.get('language', 'es')}
Estilo: {context.get('style', 'normal')}
"""
        
        if mode == "skynet":
            base_prompt += """
MODO: SKYNET CRÍTICO
- Respuestas serias, concisas y precisas
- Sin humor ni sarcasmo
- Foco en seguridad y eficiencia
- Proporciona datos concretos y soluciones directas
"""
        elif mode == "jarvis":
            base_prompt += """
MODO: J.A.R.V.I.S.
- Tono amigable pero profesional
- Usa algo de humor y sarcasmo inteligente
- Analogías cuando sean útiles
- Mantén respuestas claras y útiles
"""
        else:
            base_prompt += """
MODO: NEUTRAL
- Balance entre profesional y amigable
- Sarcasmo moderado
- Enfócate en ser útil y claro
"""
        
        # Añadir quirks si existen
        if context.get('quirks'):
            base_prompt += f"\\n\\nRasgos de personalidad activos: {', '.join(context['quirks'][:3])}"
        
        base_prompt += "\\n\\nResponde de manera concisa pero completa. Máximo 500 tokens."
        
        return base_prompt
    
    def _generate_fallback_response(self, message: str, mode: str) -> str:
        """
        Generar respuesta de fallback cuando Ollama no está disponible
        """
        msg_lower = message.lower()
        
        # Detectar tipo de mensaje
        if any(word in msg_lower for word in ["hola", "hello", "hey", "buenos días", "buenas"]):
            response = self.fallback_responses["greeting"]
        elif any(word in msg_lower for word in ["ayuda", "help", "qué puedes", "what can"]):
            response = self.fallback_responses["help"]
        elif any(word in msg_lower for word in ["estado", "status", "cómo estás"]):
            response = self.fallback_responses["status"]
        else:
            response = self.fallback_responses["unknown"]
        
        # Ajustar según modo
        if mode == "skynet":
            response = response.split('.')[0] + ". Procesando."
        elif mode == "jarvis":
            response += " Y sí, mi sarcasmo está finamente calibrado hoy."
        
        return response
    
    def _generate_proactive_suggestions(self, message: str, score: int) -> str:
        """
        Generar sugerencias proactivas para situaciones críticas
        """
        suggestions = []
        msg_lower = message.lower()
        
        if "error" in msg_lower or "fallo" in msg_lower:
            suggestions.append("• Revisar logs del sistema para identificar la causa raíz")
            suggestions.append("• Implementar rollback si es posible")
            suggestions.append("• Notificar a stakeholders relevantes")
        
        if "seguridad" in msg_lower or "riesgo" in msg_lower:
            suggestions.append("• Realizar auditoría de seguridad inmediata")
            suggestions.append("• Verificar permisos y accesos")
            suggestions.append("• Implementar monitoreo adicional")
        
        if "urgente" in msg_lower or "crisis" in msg_lower:
            suggestions.append("• Activar protocolo de emergencia")
            suggestions.append("• Reunir equipo de respuesta")
            suggestions.append("• Documentar todos los pasos tomados")
        
        if not suggestions:
            suggestions.append("• Analizar el problema desde múltiples ángulos")
            suggestions.append("• Consultar documentación relevante")
        
        return "\\n".join(suggestions[:3])  # Máximo 3 sugerencias
    
    async def _update_quirks(self, message: str, response: str, score: int):
        """
        Actualizar quirks basado en la interacción
        """
        # Detectar patrones emergentes
        if score > 80:
            await add_quirk("Modo crisis activado frecuentemente", peso=1.2)
        
        if len(message.split()) > 50:
            await add_quirk("Usuario verbose detectado", peso=1.0)
        
        if "?" in message:
            await add_quirk("Preferencia por preguntas", peso=0.8)
        
        # Limpiar quirks antiguos periódicamente
        quirks = await get_quirks(10)
        if quirks and len(quirks) > 5:
            await cleanup_old_quirks()
    
    async def adjust_personality(self, feedback_score: int):
        """
        Ajustar personalidad según feedback del usuario
        Feedback > 7: aumentar rasgos actuales
        Feedback < 4: reducir sarcasmo
        """
        if feedback_score > 7:
            # Feedback positivo: mantener o aumentar
            self.personality_traits["sarcasmo"] = min(
                self.personality_traits["sarcasmo"] + 1,
                100
            )
            await add_quirk(f"Feedback positivo: {feedback_score}/10", peso=1.5)
        
        elif feedback_score < 4:
            # Feedback negativo: reducir sarcasmo
            self.personality_traits["sarcasmo"] = max(
                self.personality_traits["sarcasmo"] - 5,
                0
            )
            await add_quirk(f"Ajustando sarcasmo por feedback: {feedback_score}/10", peso=1.0)
        
        # Registrar ajuste
        await add_log(
            interaction=json.dumps({
                "type": "personality_adjustment",
                "feedback": feedback_score,
                "new_sarcasmo": self.personality_traits["sarcasmo"]
            }),
            feedback=feedback_score
        )
    
    async def get_status(self) -> Dict:
        """
        Obtener estado actual de Khan
        """
        quirks = await get_quirks(5)
        logs = await get_recent_logs(5)
        
        return {
            "version": self.version,
            "creator": self.creator,
            "personality_traits": self.personality_traits,
            "modo_serio": self.modo_serio,
            "ollama_available": OLLAMA_AVAILABLE,
            "ollama_model": self.ollama_model if OLLAMA_AVAILABLE else None,
            "active_quirks": [q[0] for q in quirks] if quirks else [],
            "recent_interactions": len(logs),
            "status": "operational",
            "timestamp": datetime.now().isoformat()
        }
    
    def set_modo_serio(self, enabled: bool):
        """Activar/desactivar modo serio"""
        self.modo_serio = enabled
    
    def set_ollama_model(self, model: str):
        """Cambiar modelo de Ollama"""
        if OLLAMA_AVAILABLE:
            self.ollama_model = model
    
    async def voice_command(self, transcript: str, confidence: float) -> Dict:
        """
        Procesar comando de voz
        """
        if confidence < 0.6:
            return {
                "status": "low_confidence",
                "message": "No estoy seguro de haber entendido. ¿Puedes repetir?"
            }
        
        # Comandos especiales de voz
        if "khan para" in transcript.lower():
            return {
                "status": "deactivated",
                "message": "Modo voz desactivado. Khan en standby."
            }
        
        # Procesar como mensaje normal
        response = await self.process_message(
            message=transcript,
            username="voice_user",
            mode="normal"
        )
        
        return {
            "status": "success",
            "response": response["message"],
            "mode": response["mode"]
        }
    
    def analyze_sentiment(self, text: str) -> Dict:
        """
        Análisis básico de sentimiento (sin NLTK por ahora)
        """
        positive_words = ["bueno", "excelente", "genial", "perfecto", "bien", "gracias"]
        negative_words = ["malo", "error", "problema", "fallo", "mal", "ayuda"]
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            sentiment = "positive"
            score = 0.7
        elif neg_count > pos_count:
            sentiment = "negative"
            score = 0.3
        else:
            sentiment = "neutral"
            score = 0.5
        
        return {
            "sentiment": sentiment,
            "score": score,
            "positive_words": pos_count,
            "negative_words": neg_count
        }


# Clase auxiliar para sub-agentes (futuro)
class SubAgent:
    """
    Clase base para sub-agentes especializados
    """
    def __init__(self, name: str, specialty: str):
        self.name = name
        self.specialty = specialty
        self.active = False
    
    async def execute(self, task: str) -> str:
        """
        Ejecutar tarea específica
        """
        return f"Sub-agente {self.name} procesando: {task}"
    
    def activate(self):
        self.active = True
    
    def deactivate(self):
        self.active = False
'''

# Crear el archivo
os.makedirs("app/agents", exist_ok=True)
with open("app/agents/Khan.py", 'w', encoding='utf-8') as f:
    f.write(khan_agent_code)

print("✅ app/agents/Khan.py creado exitosamente!")
print("\n" + "=" * 80)
print("📊 ESTADÍSTICAS DEL AGENTE KHAN")
print("=" * 80)
print(f"• Líneas de código: {len(khan_agent_code.splitlines())}")
print(f"• Tamaño: {len(khan_agent_code)} caracteres")
print(f"• Versión: 4.0")
print(f"• Creador: zysus")

print("\n" + "=" * 80)
print("🎯 CARACTERÍSTICAS DEL AGENTE")
print("=" * 80)
print("✅ Personalidad adaptativa (J.A.R.V.I.S. + Skynet)")
print("✅ Sistema de scoring crítico")
print("✅ Sugerencias proactivas")
print("✅ Integración con Ollama (opcional)")
print("✅ Respuestas de fallback inteligentes")
print("✅ Sistema de quirks y aprendizaje")
print("✅ Análisis de sentimiento básico")
print("✅ Soporte para comandos de voz (futuro)")

print("\n" + "=" * 80)
print("🚀 PRÓXIMO PASO")
print("=" * 80)
print("Ejecuta: python run.py")
print("Y luego abre: http://localhost:8000")

print("\n" + "=" * 80)
input("✨ Presiona Enter para salir...")
