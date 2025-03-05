import logging
from typing import Dict, Any, Optional

from saga.saga_base import Saga
from checkout.models import Order, OrderStatus
from checkout.saga_steps import PaymentStep, InventoryStep, ShippingStep
from services.payment_service import PaymentService
from services.inventory_service import InventoryService
from services.shipping_service import ShippingService

logger = logging.getLogger("checkout.checkout_saga")


class CheckoutSaga:
    """
    Координатор процесса оформления заказа с использованием Saga Pattern
    """
    
    def __init__(self):
        # Инициализация сервисов
        self.payment_service = PaymentService()
        self.inventory_service = InventoryService()
        self.shipping_service = ShippingService()
        
        # Создание шагов Saga
        payment_step = PaymentStep(self.payment_service)
        inventory_step = InventoryStep(self.inventory_service)
        shipping_step = ShippingStep(self.shipping_service)
        
        # Создание Saga с последовательностью шагов
        self.saga = Saga("checkout_saga")
        self.saga.add_step(payment_step) \
                .add_step(inventory_step) \
                .add_step(shipping_step)
    
    def process_order(self, order: Order) -> bool:
        """
        Обрабатывает заказ, проводя его через все шаги Saga
        
        Args:
            order: Заказ для обработки
            
        Returns:
            bool: True если заказ обработан успешно, False в противном случае
        """
        logger.info(f"Processing order: {order}")
        
        # Создание контекста выполнения Saga
        context = {"order": order}
        
        # Выполнение Saga
        success = self.saga.execute(context)
        
        if success:
            order.update_status(OrderStatus.COMPLETED)
            logger.info(f"Order {order.id} processed successfully")
        else:
            order.update_status(OrderStatus.CANCELLED)
            logger.error(f"Order {order.id} processing failed")
        
        return success 