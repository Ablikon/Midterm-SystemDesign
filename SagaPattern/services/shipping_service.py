import logging
import uuid
import random
from typing import Dict, Any, Optional

logger = logging.getLogger("services.shipping")

class ShippingService:
    """
    Сервис для управления доставкой
    В реальном приложении это был бы сервис, интегрированный с системой доставки
    """
    
    def __init__(self, failure_probability: float = 0.2):
        """
        Инициализирует сервис доставки
        
        Args:
            failure_probability: Вероятность сбоя операции (для демонстрации компенсации)
        """
        self.shipments = {}  # Хранилище отправлений (имитация базы данных)
        self.failure_probability = failure_probability
    
    def create_shipment(self, order_id: str, product_id: str, quantity: int, customer_id: str) -> Dict[str, Any]:
        """
        Создает отправление для заказа
        
        Args:
            order_id: ID заказа
            product_id: ID продукта
            quantity: Количество товара
            customer_id: ID клиента
            
        Returns:
            Dict: Информация о результате операции
        """
        logger.info(f"Creating shipment for order {order_id}, product {product_id}, quantity {quantity}")
        
        # Имитация случайного сбоя для демонстрации компенсации
        if random.random() < self.failure_probability:
            logger.error(f"Shipment creation failed for order {order_id}")
            return {"success": False, "error": "Shipping service error"}
        
        # Генерация ID отправления
        shipment_id = str(uuid.uuid4())
        
        # Сохранение информации об отправлении
        shipment_info = {
            "id": shipment_id,
            "order_id": order_id,
            "product_id": product_id,
            "quantity": quantity,
            "customer_id": customer_id,
            "status": "created"
        }
        
        self.shipments[shipment_id] = shipment_info
        
        logger.info(f"Shipment {shipment_id} created successfully for order {order_id}")
        return {"success": True, "shipment_id": shipment_id, "status": "created"}
    
    def cancel_shipment(self, shipment_id: str) -> Dict[str, Any]:
        """
        Отменяет отправление
        
        Args:
            shipment_id: ID отправления
            
        Returns:
            Dict: Информация о результате операции
        """
        if shipment_id not in self.shipments:
            logger.error(f"Cannot cancel non-existent shipment {shipment_id}")
            return {"success": False, "error": "Shipment not found"}
        
        shipment = self.shipments[shipment_id]
        logger.info(f"Cancelling shipment {shipment_id} for order {shipment['order_id']}")
        
        # Обновление статуса отправления
        shipment["status"] = "cancelled"
        
        logger.info(f"Shipment {shipment_id} cancelled successfully")
        return {"success": True, "shipment_id": shipment_id, "status": "cancelled"}
    
    def get_shipment(self, shipment_id: str) -> Optional[Dict[str, Any]]:
        """
        Получает информацию об отправлении
        
        Args:
            shipment_id: ID отправления
            
        Returns:
            Optional[Dict]: Информация об отправлении или None, если отправление не найдено
        """
        return self.shipments.get(shipment_id)
    
    def get_shipment_by_order(self, order_id: str) -> Optional[Dict[str, Any]]:
        """
        Получает информацию об отправлении по ID заказа
        
        Args:
            order_id: ID заказа
            
        Returns:
            Optional[Dict]: Информация об отправлении или None, если отправление не найдено
        """
        for shipment in self.shipments.values():
            if shipment["order_id"] == order_id:
                return shipment
        return None 