import logging
import random
from typing import Dict, Any, Optional

logger = logging.getLogger("services.inventory")

class InventoryService:
    """
    Сервис для управления товарным запасом
    В реальном приложении это был бы сервис, интегрированный с системой управления запасами
    """
    
    def __init__(self, failure_probability: float = 0.2):
        """
        Инициализирует сервис управления запасами
        
        Args:
            failure_probability: Вероятность сбоя операции (для демонстрации компенсации)
        """
        # Имитация инвентаря с продуктами и их количеством
        self.inventory = {
            "product1": 100,
            "product2": 50,
            "product3": 25,
            "product4": 0  # Продукт, который закончился
        }
        self.reservations = {}  # Хранилище резерваций (имитация базы данных)
        self.failure_probability = failure_probability
    
    def reserve_inventory(self, order_id: str, product_id: str, quantity: int) -> Dict[str, Any]:
        """
        Резервирует товары для заказа
        
        Args:
            order_id: ID заказа
            product_id: ID продукта
            quantity: Количество для резервации
            
        Returns:
            Dict: Информация о результате операции
        """
        logger.info(f"Reserving {quantity} units of {product_id} for order {order_id}")
        
        # Имитация случайного сбоя для демонстрации компенсации
        if random.random() < self.failure_probability:
            logger.error(f"Inventory reservation failed for order {order_id}")
            return {"success": False, "error": "Inventory service error"}
        
        # Проверка наличия товара
        available = self.inventory.get(product_id, 0)
        if available < quantity:
            logger.error(f"Not enough inventory for {product_id}, requested: {quantity}, available: {available}")
            return {"success": False, "error": "Not enough inventory"}
        
        # Резервация товара
        self.inventory[product_id] -= quantity
        
        # Сохранение информации о резервации
        reservation_info = {
            "order_id": order_id,
            "product_id": product_id,
            "quantity": quantity,
            "status": "reserved"
        }
        
        self.reservations[order_id] = reservation_info
        
        logger.info(f"Successfully reserved {quantity} units of {product_id} for order {order_id}")
        return {"success": True, "reserved": True}
    
    def cancel_reservation(self, order_id: str) -> Dict[str, Any]:
        """
        Отменяет резервацию товаров для заказа
        
        Args:
            order_id: ID заказа
            
        Returns:
            Dict: Информация о результате операции
        """
        if order_id not in self.reservations:
            logger.error(f"Cannot cancel non-existent reservation for order {order_id}")
            return {"success": False, "error": "Reservation not found"}
        
        # Получение информации о резервации
        reservation = self.reservations[order_id]
        logger.info(f"Cancelling reservation of {reservation['quantity']} units of {reservation['product_id']} for order {order_id}")
        
        # Возврат товара в доступный инвентарь
        product_id = reservation["product_id"]
        quantity = reservation["quantity"]
        
        self.inventory[product_id] = self.inventory.get(product_id, 0) + quantity
        
        # Обновление статуса резервации
        reservation["status"] = "cancelled"
        
        logger.info(f"Reservation for order {order_id} cancelled successfully")
        return {"success": True, "reservation_cancelled": True}
    
    def get_reservation(self, order_id: str) -> Optional[Dict[str, Any]]:
        """
        Получает информацию о резервации
        
        Args:
            order_id: ID заказа
            
        Returns:
            Optional[Dict]: Информация о резервации или None, если резервация не найдена
        """
        return self.reservations.get(order_id) 