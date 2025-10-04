"""
Script para mejorar las respuestas de Khan en modo fallback
"""
import os

print("🔧 Actualizando respuestas de Khan...")

# Leer el archivo actual
with open("app/agents/Khan.py", 'r', encoding='utf-8') as f:
    content = f.read()

# Buscar y reemplazar el método _generate_fallback_response
old_method = '''    def _generate_fallback_response(self, message: str, mode: str) -> str:
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
        
        return response'''

new_method = '''    def _generate_fallback_response(self, message: str, mode: str) -> str:
        """
        Generar respuesta de fallback cuando Ollama no está disponible
        """
        msg_lower = message.lower()
        
        # Respuestas contextuales mejoradas
        responses_by_context = {
            # Saludos
            "greeting": [
                "Hola. Khan operacional y listo para asistir.",
                "Saludos. ¿En qué puedo ayudarte hoy?",
                "Khan a tu servicio. Sistemas online.",
            ],
            
            # Código y programación
            "code": [
                "Para programación, te recomiendo: dividir el problema, escribir pseudocódigo, implementar, probar. ¿Necesitas ayuda con algún lenguaje específico?",
                "Desarrollo de software: claridad en requisitos, código limpio, testing exhaustivo. ¿Qué tecnología estás usando?",
                "Python, JavaScript, SQL... Especifica el lenguaje y el problema para darte una solución concreta.",
            ],
            
            # Análisis y datos
            "analysis": [
                "Para análisis efectivo: define objetivos, recopila datos relevantes, usa métricas claras, interpreta resultados con contexto.",
                "Análisis de datos requiere: limpieza de datos, exploración, visualización, modelado. ¿Qué aspecto necesitas?",
                "El análisis correcto empieza con las preguntas correctas. ¿Qué intentas descubrir?",
            ],
            
            # Problemas técnicos
            "technical": [
                "Problema técnico detectado. Pasos: 1) Identifica el error exacto, 2) Revisa logs, 3) Verifica configuración, 4) Prueba soluciones incrementales.",
                "Debugging sistemático: reproduce el error, aísla la causa, implementa fix, valida solución. ¿Qué error específico tienes?",
                "Para resolver esto: documenta el comportamiento esperado vs actual, revisa cambios recientes, verifica dependencias.",
            ],
            
            # Estrategia y planificación
            "strategy": [
                "Planificación efectiva: define objetivo claro, identifica recursos, establece hitos, mide progreso, ajusta según resultados.",
                "Estrategia requiere: análisis de situación actual, definición de meta, plan de acción, métricas de éxito. ¿Cuál es tu objetivo?",
                "Para optimizar esto: evalúa opciones, calcula coste-beneficio, prioriza por impacto, ejecuta con agilidad.",
            ],
            
            # Seguridad
            "security": [
                "Seguridad crítica. Prioridades: autenticación robusta, encriptación de datos sensibles, auditoría de accesos, actualizaciones regulares.",
                "Protocolo de seguridad: evalúa vulnerabilidades, implementa capas de protección, monitorea actividad, responde rápido a incidentes.",
                "Seguridad no es opcional. Revisa: permisos, autenticación, datos expuestos, logs de acceso. ¿Dónde está la brecha?",
            ],
            
            # Aprendizaje
            "learning": [
                "Para aprender efectivamente: comienza con fundamentos, practica activamente, construye proyectos reales, itera y mejora.",
                "El aprendizaje es iterativo: teoría + práctica + feedback. ¿Qué tecnología quieres dominar?",
                "Aprende haciendo: proyectos pequeños, incrementa complejidad, consulta documentación, experimenta sin miedo al error.",
            ],
            
            # General/Desconocido
            "unknown": [
                "Procesa tu consulta. Para respuesta óptima, proporciona más contexto: ¿qué intentas lograr? ¿qué has probado?",
                "Entiendo tu pregunta. Detalles adicionales ayudarían: objetivo, contexto actual, restricciones específicas.",
                "Consulta recibida. Para asistencia precisa: especifica el problema, entorno, y resultado deseado.",
            ]
        }
        
        # Detección de contexto mejorada
        context = "unknown"
        
        # Palabras clave por contexto
        if any(word in msg_lower for word in ["hola", "hello", "hey", "buenos", "buenas", "qué tal"]):
            context = "greeting"
        elif any(word in msg_lower for word in ["código", "programar", "function", "class", "python", "javascript", "sql", "bug", "syntax"]):
            context = "code"
        elif any(word in msg_lower for word in ["analizar", "análisis", "datos", "estadística", "métricas", "dashboard"]):
            context = "analysis"
        elif any(word in msg_lower for word in ["error", "fallo", "no funciona", "problema técnico", "crash", "bug"]):
            context = "technical"
        elif any(word in msg_lower for word in ["estrategia", "plan", "optimizar", "mejorar", "eficiencia", "proyecto"]):
            context = "strategy"
        elif any(word in msg_lower for word in ["seguridad", "vulnerabilidad", "ataque", "proteger", "encriptar", "autenticación"]):
            context = "security"
        elif any(word in msg_lower for word in ["aprender", "tutorial", "cómo", "enseñar", "curso", "estudiar"]):
            context = "learning"
        
        # Seleccionar respuesta según contexto
        response = random.choice(responses_by_context.get(context, responses_by_context["unknown"]))
        
        # Ajustar según modo
        if mode == "skynet":
            # Modo serio: directo y sin adornos
            response = response.split('.')[0] + '.'
            if len(response) < 50:  # Si la respuesta es muy corta, añadir acción
                response += " Especifica detalles para análisis preciso."
        elif mode == "jarvis":
            # Modo J.A.R.V.I.S.: añadir toque de personalidad
            if context == "greeting":
                response += " ¿Otro desafío intelectual hoy?"
            elif random.random() < 0.3:  # 30% de las veces añade sarcasmo
                sarcastic_endings = [
                    " Aunque seguro ya lo sabías.",
                    " Fácil, ¿verdad?",
                    " Básico, pero efectivo.",
                ]
                response += random.choice(sarcastic_endings)
        
        return response'''

# Actualizar el contenido
if old_method in content:
    content = content.replace(old_method, new_method)
    
    # Guardar el archivo actualizado
    with open("app/agents/Khan.py", 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Khan.py actualizado exitosamente!")
    print("\n📊 Mejoras aplicadas:")
    print("   ✅ Respuestas contextuales inteligentes")
    print("   ✅ Detección de 8 contextos diferentes")
    print("   ✅ Múltiples respuestas por contexto")
    print("   ✅ Modo Skynet más inteligente")
    print("   ✅ Modo J.A.R.V.I.S. con más personalidad")
    print("\n🎯 Contextos detectados:")
    print("   • Saludos")
    print("   • Código/Programación")
    print("   • Análisis de datos")
    print("   • Problemas técnicos")
    print("   • Estrategia")
    print("   • Seguridad")
    print("   • Aprendizaje")
    print("   • General")
    
else:
    print("⚠️  No se encontró el método a actualizar.")
    print("   El archivo Khan.py podría estar modificado.")
    print("   Revisa manualmente el método _generate_fallback_response")

print("\n🚀 Reinicia Khan AI para aplicar los cambios:")
print("   python run.py")

input("\nPresiona Enter para salir...")
