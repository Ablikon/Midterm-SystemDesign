import logging
from typing import Dict, Any

from saga.saga_base import SagaStep
from checkout.models import Order, OrderStatus
from services.payment_service import PaymentService
from services.inventory_service import InventoryService
from services.shipping_service import ShippingService

logger = logging.getLogger("checkout.saga_steps")


class PaymentStep(SagaStep):
    """Шаг Saga для обработки платежа"""
    
    def __init__(self, payment_service: PaymentService):
        self.payment_service = payment_service
    
    def execute(self, context: Dict[str, Any]) -> bool:
        """
        Выполняет платеж для заказа
        
        Args:
            context: Контекст выполнения саги, должен содержать заказ в поле "order"
            
        Returns:
            bool: True если платеж успешен, False в противном случае
        """
        order = context["order"]
        order.update_status(OrderStatus.PAYMENT_PENDING)
        
        # Обработка платежа
        result = self.payment_service.process_payment(
            order_id=order.id,
            customer_id=order.customer_id,
            amount=order.total_amount
        )
        
        if result["success"]:
            order.payment_id = result["payment_id"]
            order.payment_status = result["status"]
            order.update_status(OrderStatus.PAYMENT_COMPLETED)
            logger.info(f"Payment step successful for order {order.id}")
            return True
        else:
            order.update_status(OrderStatus.PAYMENT_FAILED)
            logger.error(f"Payment step failed for order {order.id}: {result.get('error', 'Unknown error')}")
            return False
    
    def compensate(self, context: Dict[str, Any]) -> None:
        """
        Возвращает средства клиенту
        
        Args:
            context: Контекст выполнения саги
        """
        order = context["order"]
        if order.payment_id:
            result = self.payment_service.refund_payment(order.payment_id)
            if result["success"]:
                order.payment_status = result["status"]
                logger.info(f"Payment refunded for order {order.id}")
            else:
                logger.error(f"Failed to refund payment for order {order.id}: {result.get('error', 'Unknown error')}")
        else:
            logger.info(f"No payment to refund for order {order.id}")


class InventoryStep(SagaStep):
    """Шаг Saga для резервации товаров"""
    
    def __init__(self, inventory_service: InventoryService):
        self.inventory_service = inventory_service
    
    def execute(self, context: Dict[str, Any]) -> bool:
        """
        Резервирует товары для заказа
        
        Args:
            context: Контекст выполнения саги, должен содержать заказ в поле "order"
            
        Returns:
            bool: True если резервация успешна, False в противном случае
        """
        order = context["order"]
        order.update_status(OrderStatus.INVENTORY_PENDING)
        
        # Резервация товаров
        result = self.inventory_service.reserve_inventory(
            order_id=order.id,
            product_id=order.product_id,
            quantity=order.quantity
        )
        
        if result["success"]:
            order.inventory_reserved = True
            order.update_status(OrderStatus.INVENTORY_RESERVED)
            logger.info(f"Inventory step successful for order {order.id}")
            return True
        else:
            order.update_status(OrderStatus.INVENTORY_FAILED)
            logger.error(f"Inventory step failed for order {order.id}: {result.get('error', 'Unknown error')}")
            return False
    
    def compensate(self, context: Dict[str, Any]) -> None:
        """
        Отменяет резервацию товаров
        
        Args:
            context: Контекст выполнения саги
        """
        order = context["order"]
        if order.inventory_reserved:
            result = self.inventory_service.cancel_reservation(order.id)
            if result["success"]:
                order.inventory_reserved = False
                logger.info(f"Inventory reservation cancelled for order {order.id}")
            else:
                logger.error(f"Failed to cancel inventory reservation for order {order.id}: {result.get('error', 'Unknown error')}")
        else:
            logger.info(f"No inventory reservation to cancel for order {order.id}")


class ShippingStep(SagaStep):
    """Шаг Saga для создания отправления"""
    
    def __init__(self, shipping_service: ShippingService):
        self.shipping_service = shipping_service
    
    def execute(self, context: Dict[str, Any]) -> bool:
        """
        Создает отправление для заказа
        
        Args:
            context: Контекст выполнения саги, должен содержать заказ в поле "order"
            
        Returns:
            bool: True если создание отправления успешно, False в противном случае
        """
        order = context["order"]
        order.update_status(OrderStatus.SHIPPING_PENDING)
        
        # Создание отправления
        result = self.shipping_service.create_shipment(
            order_id=order.id,
            product_id=order.product_id,
            quantity=order.quantity,
            customer_id=order.customer_id
        )
        
        if result["success"]:
            order.shipping_id = result["shipment_id"]
            order.shipping_status = result["status"]
            order.update_status(OrderStatus.SHIPPING_COMPLETED)
            logger.info(f"Shipping step successful for order {order.id}")
            return True
        else:
            order.update_status(OrderStatus.SHIPPING_FAILED)
            logger.error(f"Shipping step failed for order {order.id}: {result.get('error', 'Unknown error')}")
            return False
    
    def compensate(self, context: Dict[str, Any]) -> None:
        """
        Отменяет отправление
        
        Args:
            context: Контекст выполнения саги
        """
        order = context["order"]
        if order.shipping_id:
            result = self.shipping_service.cancel_shipment(order.shipping_id)
            if result["success"]:
                order.shipping_status = result["status"]
                logger.info(f"Shipment cancelled for order {order.id}")
            else:
                logger.error(f"Failed to cancel shipment for order {order.id}: {result.get('error', 'Unknown error')}")
        else:
            logger.info(f"No shipment to cancel for order {order.id}") 