import logging
import sys
import time
import random
from typing import List, Dict, Any

from checkout.models import Order
from checkout.checkout_saga import CheckoutSaga
from services.payment_service import PaymentService
from services.inventory_service import InventoryService
from services.shipping_service import ShippingService

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("example")

def run_successful_checkout():
    """Запускает успешный процесс оформления заказа"""
    logger.info("\n\n=== STARTING SUCCESSFUL CHECKOUT ===\n")
    
    # Создаем заказ
    order = Order(
        customer_id="customer123",
        product_id="product1",  # Этот продукт доступен в инвентаре
        quantity=2,
        total_amount=99.99
    )
    
    # Создаем сагу для обработки заказа
    # Устанавливаем низкую вероятность сбоя для успешного выполнения
    checkout_saga = create_saga_with_failure_probability(0.0)
    
    # Обрабатываем заказ
    success = checkout_saga.process_order(order)
    
    # Выводим результат
    if success:
        logger.info(f"Checkout completed successfully: {order}")
    else:
        logger.error(f"Checkout failed: {order}")
        
    return success

def run_failed_inventory_checkout():
    """Запускает процесс оформления заказа с ошибкой на шаге инвентаря"""
    logger.info("\n\n=== STARTING CHECKOUT WITH INVENTORY FAILURE ===\n")
    
    # Создаем заказ с продуктом, которого нет в наличии
    order = Order(
        customer_id="customer456",
        product_id="product4",  # Этот продукт недоступен в инвентаре
        quantity=5,
        total_amount=199.99
    )
    
    # Создаем сагу для обработки заказа
    checkout_saga = create_saga_with_failure_probability(0.0)
    
    # Обрабатываем заказ
    success = checkout_saga.process_order(order)
    
    # Выводим результат
    if success:
        logger.info(f"Checkout completed successfully: {order}")
    else:
        logger.error(f"Checkout failed at inventory step: {order}")
        
    return success

def run_failed_shipping_checkout():
    """Запускает процесс оформления заказа с ошибкой на шаге доставки"""
    logger.info("\n\n=== STARTING CHECKOUT WITH SHIPPING FAILURE ===\n")
    
    # Создаем заказ
    order = Order(
        customer_id="customer789",
        product_id="product2",
        quantity=3,
        total_amount=149.99
    )
    
    # Создаем сагу для обработки заказа
    # Устанавливаем высокую вероятность сбоя только для шага доставки
    checkout_saga = CheckoutSaga()
    checkout_saga.payment_service.failure_probability = 0.0
    checkout_saga.inventory_service.failure_probability = 0.0
    checkout_saga.shipping_service.failure_probability = 1.0  # 100% сбой
    
    # Обрабатываем заказ
    success = checkout_saga.process_order(order)
    
    # Выводим результат
    if success:
        logger.info(f"Checkout completed successfully: {order}")
    else:
        logger.error(f"Checkout failed at shipping step: {order}")
        
    return success

def create_saga_with_failure_probability(probability: float) -> CheckoutSaga:
    """
    Создает сагу с заданной вероятностью сбоя для всех сервисов
    
    Args:
        probability: Вероятность сбоя для каждого сервиса
        
    Returns:
        CheckoutSaga: Готовая сага с настроенными сервисами
    """
    checkout_saga = CheckoutSaga()
    checkout_saga.payment_service.failure_probability = probability
    checkout_saga.inventory_service.failure_probability = probability
    checkout_saga.shipping_service.failure_probability = probability
    
    return checkout_saga

def run_random_checkouts(count: int):
    """
    Запускает несколько случайных процессов оформления заказа
    
    Args:
        count: Количество заказов для обработки
    """
    logger.info(f"\n\n=== STARTING {count} RANDOM CHECKOUTS ===\n")
    
    products = ["product1", "product2", "product3", "product4"]
    success_count = 0
    
    for i in range(count):
        logger.info(f"\n--- Random Checkout #{i+1} ---\n")
        
        # Случайный продукт и количество
        product_id = random.choice(products)
        quantity = random.randint(1, 10)
        total_amount = quantity * random.uniform(10.0, 100.0)
        
        # Создаем заказ
        order = Order(
            customer_id=f"customer_{i}",
            product_id=product_id,
            quantity=quantity,
            total_amount=total_amount
        )
        
        # Создаем сагу со случайной вероятностью сбоя
        checkout_saga = create_saga_with_failure_probability(random.uniform(0.0, 0.3))
        
        # Обрабатываем заказ
        success = checkout_saga.process_order(order)
        if success:
            success_count += 1
            
        # Небольшая пауза между заказами для лучшей читаемости логов
        time.sleep(0.5)
    
    logger.info(f"\nCompleted {count} random checkouts. Success rate: {success_count}/{count} ({success_count/count*100:.1f}%)")

if __name__ == "__main__":
    # Запускаем демонстрацию различных сценариев
    run_successful_checkout()
    run_failed_inventory_checkout()
    run_failed_shipping_checkout()
    
    # Запускаем несколько случайных заказов
    run_random_checkouts(5) 