from abc import ABC, abstractmethod
from typing import List, Callable, Dict, Any
import logging

# Настройка логгера
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("saga")


class SagaStep(ABC):
    """Абстрактный базовый класс для шага Saga"""
    
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> bool:
        """
        Выполнить шаг саги (действие 'do')
        
        Args:
            context: Контекст выполнения саги (данные, общие для всех шагов)
            
        Returns:
            bool: True если шаг выполнен успешно, False в противном случае
        """
        pass
    
    @abstractmethod
    def compensate(self, context: Dict[str, Any]) -> None:
        """
        Компенсировать выполненный шаг (действие 'compensate')
        
        Args:
            context: Контекст выполнения саги
        """
        pass


class Saga:
    """
    Класс, управляющий последовательностью шагов Saga
    и компенсацией в случае ошибки
    """
    
    def __init__(self, name: str):
        self.name = name
        self.steps: List[SagaStep] = []
        self.completed_steps: List[SagaStep] = []
        self.logger = logging.getLogger(f"saga.{name}")
    
    def add_step(self, step: SagaStep) -> 'Saga':
        """
        Добавляет шаг в сагу
        
        Args:
            step: Шаг для добавления
            
        Returns:
            self: Для цепочки вызовов
        """
        self.steps.append(step)
        return self
    
    def execute(self, context: Dict[str, Any]) -> bool:
        """
        Выполняет все шаги саги по порядку
        
        Args:
            context: Контекст выполнения саги
            
        Returns:
            bool: True если все шаги выполнены успешно, False иначе
        """
        self.logger.info(f"Starting saga: {self.name}")
        self.completed_steps = []
        
        for step in self.steps:
            step_name = step.__class__.__name__
            self.logger.info(f"Executing step: {step_name}")
            
            success = step.execute(context)
            if success:
                self.logger.info(f"Step {step_name} completed successfully")
                self.completed_steps.append(step)
            else:
                self.logger.error(f"Step {step_name} failed, starting compensation")
                self._compensate(context)
                return False
        
        self.logger.info(f"Saga {self.name} completed successfully")
        return True
    
    def _compensate(self, context: Dict[str, Any]) -> None:
        """
        Компенсирует выполненные шаги в обратном порядке
        
        Args:
            context: Контекст выполнения саги
        """
        self.logger.info(f"Starting compensation for saga: {self.name}")
        
        # Обратный порядок для компенсации
        for step in reversed(self.completed_steps):
            step_name = step.__class__.__name__
            self.logger.info(f"Compensating step: {step_name}")
            
            try:
                step.compensate(context)
                self.logger.info(f"Step {step_name} compensated successfully")
            except Exception as e:
                self.logger.error(f"Error during compensation of step {step_name}: {str(e)}")
        
        self.logger.info(f"Compensation for saga {self.name} completed") 