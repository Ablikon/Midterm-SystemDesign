import logging
import uuid
import random
from typing import Dict, Any, Optional

logger = logging.getLogger("services.payment")

class PaymentService:
    """
    Сервис для обработки платежей
    В реальном приложении это был бы сервис, интегрированный с платежной системой
    """
    
    def __init__(self, failure_probability: float = 0.2):
        """
        Инициализирует сервис платежей
        
        Args:
            failure_probability: Вероятность сбоя операции (для демонстрации компенсации)
        """
        self.payments = {}  # Хранилище платежей (имитация базы данных)
        self.failure_probability = failure_probability
    
    def process_payment(self, order_id: str, customer_id: str, amount: float) -> Dict[str, Any]:
        """
        Обрабатывает платеж для заказа
        
        Args:
            order_id: ID заказа
            customer_id: ID клиента
            amount: Сумма платежа
            
        Returns:
            Dict: Информация о платеже
        """
        logger.info(f"Processing payment for order {order_id}, amount: ${amount:.2f}")
        
        # Имитация случайного сбоя для демонстрации компенсации
        if random.random() < self.failure_probability:
            logger.error(f"Payment processing failed for order {order_id}")
            return {"success": False, "error": "Payment gateway error"}
        
        # Генерация ID платежа
        payment_id = str(uuid.uuid4())
        
        # Сохранение информации о платеже
        payment_info = {
            "id": payment_id,
            "order_id": order_id,
            "customer_id": customer_id,
            "amount": amount,
            "status": "completed"
        }
        
        self.payments[payment_id] = payment_info
        
        logger.info(f"Payment {payment_id} processed successfully for order {order_id}")
        return {"success": True, "payment_id": payment_id, "status": "completed"}
    
    def refund_payment(self, payment_id: str) -> Dict[str, Any]:
        """
        Возвращает средства клиенту (отмена платежа)
        
        Args:
            payment_id: ID платежа для возврата
            
        Returns:
            Dict: Информация о результате операции
        """
        if payment_id not in self.payments:
            logger.error(f"Cannot refund non-existent payment {payment_id}")
            return {"success": False, "error": "Payment not found"}
        
        payment = self.payments[payment_id]
        logger.info(f"Refunding payment {payment_id} for order {payment['order_id']}, amount: ${payment['amount']:.2f}")
        
        # Обновляем статус платежа
        payment["status"] = "refunded"
        
        logger.info(f"Payment {payment_id} refunded successfully")
        return {"success": True, "payment_id": payment_id, "status": "refunded"}
    
    def get_payment(self, payment_id: str) -> Optional[Dict[str, Any]]:
        """
        Получает информацию о платеже
        
        Args:
            payment_id: ID платежа
            
        Returns:
            Optional[Dict]: Информация о платеже или None, если платеж не найден
        """
        return self.payments.get(payment_id) 