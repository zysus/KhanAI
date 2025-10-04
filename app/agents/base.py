"""
Base Agent Class - Clase base para todos los agentes
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime


class BaseAgent(ABC):
    """
    Clase base abstracta para todos los agentes del sistema Khan
    """
    
    def __init__(self, name: str, version: str = "1.0"):
        self.name = name
        self.version = version
        self.created_at = datetime.now()
        self.active = False
        self.interaction_count = 0
    
    @abstractmethod
    async def process_message(self, message: str, **kwargs) -> Dict[str, Any]:
        """
        Procesar un mensaje - debe ser implementado por cada agente
        """
        pass
    
    @abstractmethod
    async def get_status(self) -> Dict[str, Any]:
        """
        Obtener estado del agente
        """
        pass
    
    def activate(self):
        """Activar el agente"""
        self.active = True
    
    def deactivate(self):
        """Desactivar el agente"""
        self.active = False
    
    def increment_interaction(self):
        """Incrementar contador de interacciones"""
        self.interaction_count += 1
    
    def get_basic_info(self) -> Dict[str, Any]:
        """Obtener información básica del agente"""
        return {
            "name": self.name,
            "version": self.version,
            "active": self.active,
            "created_at": self.created_at.isoformat(),
            "interaction_count": self.interaction_count
        }


class SpecializedAgent(BaseAgent):
    """
    Agente especializado con una tarea específica
    """
    
    def __init__(self, name: str, specialty: str, version: str = "1.0"):
        super().__init__(name, version)
        self.specialty = specialty
        self.success_rate = 0.0
        self.total_tasks = 0
        self.successful_tasks = 0
    
    async def process_message(self, message: str, **kwargs) -> Dict[str, Any]:
        """
        Procesamiento básico - puede ser sobreescrito
        """
        self.increment_interaction()
        return {
            "agent": self.name,
            "specialty": self.specialty,
            "message": f"Procesando con especialidad: {self.specialty}",
            "status": "processing"
        }
    
    async def get_status(self) -> Dict[str, Any]:
        """
        Estado del agente especializado
        """
        info = self.get_basic_info()
        info.update({
            "specialty": self.specialty,
            "success_rate": self.success_rate,
            "total_tasks": self.total_tasks,
            "successful_tasks": self.successful_tasks
        })
        return info
    
    def record_task_result(self, success: bool):
        """Registrar resultado de una tarea"""
        self.total_tasks += 1
        if success:
            self.successful_tasks += 1
        
        if self.total_tasks > 0:
            self.success_rate = self.successful_tasks / self.total_tasks