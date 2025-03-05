import unittest
import logging
import sys
import os

# Добавляем родительскую директорию в путь поиска модулей
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from checkout.models import Order, OrderStatus
from checkout.checkout_saga import CheckoutSaga

# Отключаем логгирование при выполнении тестов
logging.basicConfig(level=logging.CRITICAL)


class TestCheckoutSaga(unittest.TestCase):
    """Тесты для демонстрации работы Saga Pattern в процессе оформления заказа"""
    
    def setUp(self):
        """Подготовка тестов"""
        # Создаем сагу для тестирования
        self.checkout_saga = CheckoutSaga()
        
        # Устанавливаем предсказуемое поведение для тестов
        self.checkout_saga.payment_service.failure_probability = 0.0
        self.checkout_saga.inventory_service.failure_probability = 0.0
        self.checkout_saga.shipping_service.failure_probability = 0.0
    
    def test_successful_checkout(self):
        """Проверка успешного сценария оформления заказа"""
        # Создаем заказ с доступным продуктом
        order = Order(
            customer_id="test_customer",
            product_id="product1",  # Доступный продукт
            quantity=1,
            total_amount=50.0
        )
        
        # Запускаем процесс оформления заказа
        success = self.checkout_saga.process_order(order)
        
        # Проверки результатов
        self.assertTrue(success, "Checkout process should succeed")
        self.assertEqual(order.status, OrderStatus.COMPLETED, "Order status should be COMPLETED")
        self.assertIsNotNone(order.payment_id, "Payment ID should be set")
        self.assertTrue(order.inventory_reserved, "Inventory should be reserved")
        self.assertIsNotNone(order.shipping_id, "Shipping ID should be set")
    
    def test_inventory_failure_with_compensation(self):
        """Проверка сценария с ошибкой на шаге инвентаря и компенсацией"""
        # Создаем заказ с недоступным продуктом
        order = Order(
            customer_id="test_customer",
            product_id="product4",  # Недоступный продукт (нет в наличии)
            quantity=10,
            total_amount=100.0
        )
        
        # Запускаем процесс оформления заказа
        success = self.checkout_saga.process_order(order)
        
        # Проверки результатов
        self.assertFalse(success, "Checkout process should fail")
        self.assertEqual(order.status, OrderStatus.CANCELLED, "Order status should be CANCELLED")
        self.assertIsNotNone(order.payment_id, "Payment ID should be set")
        self.assertEqual(order.payment_status, "refunded", "Payment should be refunded")
        self.assertFalse(order.inventory_reserved, "Inventory should not be reserved")
    
    def test_shipping_failure_with_compensation(self):
        """Проверка сценария с ошибкой на шаге доставки и компенсацией"""
        # Создаем обычный заказ
        order = Order(
            customer_id="test_customer",
            product_id="product2",
            quantity=2,
            total_amount=150.0
        )
        
        # Устанавливаем 100% вероятность сбоя на шаге доставки
        self.checkout_saga.shipping_service.failure_probability = 1.0
        
        # Запускаем процесс оформления заказа
        success = self.checkout_saga.process_order(order)
        
        # Проверки результатов
        self.assertFalse(success, "Checkout process should fail")
        self.assertEqual(order.status, OrderStatus.CANCELLED, "Order status should be CANCELLED")
        self.assertIsNotNone(order.payment_id, "Payment ID should be set")
        self.assertEqual(order.payment_status, "refunded", "Payment should be refunded")
        self.assertFalse(order.inventory_reserved, "Inventory reservation should be cancelled")
    
    def test_payment_failure(self):
        """Проверка сценария с ошибкой на шаге платежа"""
        # Создаем заказ
        order = Order(
            customer_id="test_customer",
            product_id="product3",
            quantity=3,
            total_amount=200.0
        )
        
        # Устанавливаем 100% вероятность сбоя на шаге платежа
        self.checkout_saga.payment_service.failure_probability = 1.0
        
        # Запускаем процесс оформления заказа
        success = self.checkout_saga.process_order(order)
        
        # Проверки результатов
        self.assertFalse(success, "Checkout process should fail")
        self.assertEqual(order.status, OrderStatus.CANCELLED, "Order status should be CANCELLED")
        self.assertIsNone(order.payment_id, "Payment ID should not be set")
        self.assertFalse(order.inventory_reserved, "Inventory should not be reserved")
        self.assertIsNone(order.shipping_id, "Shipping ID should not be set")


if __name__ == "__main__":
    unittest.main() 