from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
import uuid
from datetime import datetime


class OrderStatus(Enum):
    """Статусы заказа в процессе обработки"""
    CREATED = auto()
    PAYMENT_PENDING = auto()
    PAYMENT_COMPLETED = auto()
    PAYMENT_FAILED = auto()
    INVENTORY_PENDING = auto()
    INVENTORY_RESERVED = auto()
    INVENTORY_FAILED = auto()
    SHIPPING_PENDING = auto()
    SHIPPING_COMPLETED = auto()
    SHIPPING_FAILED = auto()
    COMPLETED = auto()
    CANCELLED = auto()


@dataclass
class Order:
    """Класс для представления заказа в системе электронной коммерции"""
    customer_id: str
    product_id: str
    quantity: int
    total_amount: float
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: OrderStatus = OrderStatus.CREATED
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    # Информация о платеже
    payment_id: Optional[str] = None
    payment_status: Optional[str] = None
    
    # Информация об инвентаре
    inventory_reserved: bool = False
    
    # Информация о доставке
    shipping_id: Optional[str] = None
    shipping_status: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразует заказ в словарь для передачи между шагами саги"""
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "total_amount": self.total_amount,
            "status": self.status.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "payment_id": self.payment_id,
            "payment_status": self.payment_status,
            "inventory_reserved": self.inventory_reserved,
            "shipping_id": self.shipping_id,
            "shipping_status": self.shipping_status
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Order':
        """Создает заказ из словаря"""
        order = cls(
            customer_id=data["customer_id"],
            product_id=data["product_id"],
            quantity=data["quantity"],
            total_amount=data["total_amount"]
        )
        
        order.id = data["id"]
        order.status = OrderStatus[data["status"]]
        order.created_at = datetime.fromisoformat(data["created_at"])
        order.updated_at = datetime.fromisoformat(data["updated_at"])
        order.payment_id = data.get("payment_id")
        order.payment_status = data.get("payment_status")
        order.inventory_reserved = data.get("inventory_reserved", False)
        order.shipping_id = data.get("shipping_id")
        order.shipping_status = data.get("shipping_status")
        
        return order
    
    def update_status(self, status: OrderStatus) -> None:
        """Обновляет статус заказа и время обновления"""
        self.status = status
        self.updated_at = datetime.now()
    
    def __str__(self) -> str:
        return (f"Order(id={self.id}, customer={self.customer_id}, "
                f"product={self.product_id}, quantity={self.quantity}, "
                f"amount=${self.total_amount:.2f}, status={self.status.name})") 