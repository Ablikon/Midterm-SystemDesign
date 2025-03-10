# Реализация Saga Pattern в микросервисе электронной коммерции

Этот проект демонстрирует реализацию паттерна Saga в рамках одного микросервиса для процесса оформления заказа (checkout) в системе электронной коммерции.

## Содержание

- [Обзор](#обзор)
- [Описание паттерна Saga](#описание-паттерна-saga)
- [Архитектура решения](#архитектура-решения)
- [Структура проекта](#структура-проекта)
- [Запуск проекта](#запуск-проекта)
- [Примеры использования](#примеры-использования)
- [Подробности реализации](#подробности-реализации)

## Обзор

Проект моделирует процесс оформления заказа (checkout) в системе электронной коммерции, который состоит из трех основных шагов:

1. **Платеж (Payment)** - обработка платежа клиента
2. **Инвентарь (Inventory)** - резервация товаров на складе
3. **Доставка (Shipping)** - создание отправления

Каждый из этих шагов может завершиться успешно или с ошибкой. В случае ошибки на любом шаге, все ранее выполненные шаги должны быть компенсированы в обратном порядке, чтобы сохранить целостность данных и бизнес-логику.

## Описание паттерна Saga

**Saga Pattern** - это паттерн проектирования распределенных транзакций, который помогает поддерживать консистентность данных в распределенных системах, таких как микросервисная архитектура.

**Ключевые концепции Saga:**

1. **Последовательность локальных транзакций**: Каждая Saga состоит из последовательности локальных транзакций, где каждая транзакция обновляет данные внутри одного сервиса.

2. **Компенсирующие действия**: Для каждой транзакции определена соответствующая компенсирующая транзакция, которая отменяет изменения в случае сбоя.

3. **Координация Saga**: Координатор Saga отслеживает выполнение всех транзакций и инициирует компенсирующие действия при необходимости.

**Типы Saga:**

1. **Хореография (Choreography)**: Каждый сервис публикует события, которые запускают локальные транзакции в других сервисах.
2. **Оркестрация (Orchestration)**: Центральный координатор управляет всеми транзакциями и компенсациями.

В данном проекте используется подход **оркестрации**, где класс `Saga` выступает в роли координатора.

## Архитектура решения

Решение основано на следующей архитектуре:

1. **Класс Saga**: Центральный координатор, который управляет последовательностью шагов транзакции и компенсирующими действиями.

2. **Шаги Saga (SagaStep)**: Каждый шаг реализует два метода:

   - `execute()` - выполняет локальную транзакцию
   - `compensate()` - отменяет изменения, внесенные транзакцией

3. **Сервисы**: Представляют собой бизнес-логику для каждого шага:

   - `PaymentService` - обработка платежей
   - `InventoryService` - управление запасами
   - `ShippingService` - управление доставкой

4. **Контекст выполнения**: Общее состояние, которое передается между шагами Saga. В данном случае содержит объект заказа (`Order`).

## Структура проекта

```
SagaPattern/
├── __init__.py                      # Пакет Python
├── saga/                           # Базовая реализация Saga Pattern
│   ├── __init__.py
│   └── saga_base.py                # Базовые классы Saga и SagaStep
├── checkout/                       # Реализация процесса оформления заказа
│   ├── __init__.py
│   ├── models.py                   # Модели заказа и статусы
│   ├── saga_steps.py               # Шаги Saga для процесса оформления заказа
│   └── checkout_saga.py            # Координатор Saga для оформления заказа
├── services/                       # Сервисы для бизнес-логики
│   ├── __init__.py
│   ├── payment_service.py          # Сервис обработки платежей
│   ├── inventory_service.py        # Сервис управления запасами
│   └── shipping_service.py         # Сервис управления доставкой
├── example.py                      # Пример использования Saga
├── requirements.txt                # Зависимости проекта
└── README.md                       # Этот файл
```

## Запуск проекта

### Требования

- Python 3.7+

### Установка

Клонируйте репозиторий:

```bash
git clone <repository-url>
cd SagaPattern
```

### Запуск примера

```bash
python example.py
```

Или для запуска тестов:

```bash
python -m unittest discover tests
```

Это запустит демонстрацию различных сценариев процесса оформления заказа, включая успешное выполнение и различные виды сбоев с последующей компенсацией.

## Примеры использования

### 1. Успешное оформление заказа

```python
from checkout.models import Order
from checkout.checkout_saga import CheckoutSaga

# Создаем заказ
order = Order(
    customer_id="customer123",
    product_id="product1",
    quantity=2,
    total_amount=99.99
)

# Создаем координатор Saga
checkout_saga = CheckoutSaga()

# Обрабатываем заказ
success = checkout_saga.process_order(order)

if success:
    print(f"Заказ {order.id} успешно оформлен")
else:
    print(f"Ошибка оформления заказа {order.id}")
```

### 2. Обработка сбоя и компенсация

Пример из файла `example.py` показывает, как происходит обработка сбоя на этапе доставки:

```python
def run_failed_shipping_checkout():
    """Запускает процесс оформления заказа с ошибкой на шаге доставки"""
    # Создаем заказ
    order = Order(
        customer_id="customer789",
        product_id="product2",
        quantity=3,
        total_amount=149.99
    )

    # Настраиваем Saga с высокой вероятностью сбоя для доставки
    checkout_saga = CheckoutSaga()
    checkout_saga.payment_service.failure_probability = 0.0
    checkout_saga.inventory_service.failure_probability = 0.0
    checkout_saga.shipping_service.failure_probability = 1.0  # 100% сбой

    # Обрабатываем заказ (будет сбой на шаге доставки)
    success = checkout_saga.process_order(order)

    # Проверяем результат (ожидается failure)
    if not success:
        print("Произошел сбой на шаге доставки, все предыдущие шаги компенсированы")
```

## Подробности реализации

### Workflow обработки заказа

1. **Создание заказа**: Заказ создается с начальным статусом `CREATED`
2. **Платеж**:
   - `execute()`: Обрабатывает платеж, обновляет статус заказа на `PAYMENT_COMPLETED`
   - `compensate()`: Возвращает средства клиенту
3. **Инвентарь**:
   - `execute()`: Резервирует товары на складе, обновляет статус заказа на `INVENTORY_RESERVED`
   - `compensate()`: Отменяет резервацию товаров
4. **Доставка**:
   - `execute()`: Создает отправление, обновляет статус заказа на `SHIPPING_COMPLETED`
   - `compensate()`: Отменяет отправление
5. **Завершение**: Если все шаги успешны, заказ получает статус `COMPLETED`. В противном случае - `CANCELLED`.

### Обработка ошибок и компенсация

Если на любом из шагов происходит ошибка:

1. Текущий шаг помечается как неудачный
2. Координатор Saga инициирует компенсацию для всех ранее выполненных шагов в обратном порядке
3. Каждый шаг выполняет свою компенсирующую логику
4. Заказ получает финальный статус `CANCELLED`

### Расширение для микросервисной архитектуры

Хотя данная реализация создана в рамках одного сервиса, ее легко адаптировать для распределенной микросервисной архитектуры с помощью:

1. **Асинхронной коммуникации**: Использование сообщений и очередей (например, RabbitMQ или Kafka) для взаимодействия между сервисами
2. **Сохранения состояния**: Использование базы данных для сохранения состояния Saga
3. **Идемпотентности**: Обеспечение идемпотентности для всех операций, чтобы их можно было безопасно повторять

## Автор

[Ваше имя]

## Лицензия

[Укажите лицензию проекта]
