from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass
class Category:
    name: str
    description: Optional[str] = None
    id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Product:
    name: str
    price: Decimal
    stock: int = 0
    is_available: bool = True
    description: Optional[str] = None
    category_id: Optional[int] = None
    id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def reserve(self, quantity: int) -> None:
        """Бизнес-правило: списать со склада."""
        from app.domain.exceptions import OutOfStockError
        if not self.is_available or self.stock < quantity:
            raise OutOfStockError(self.name, self.stock, quantity)
        self.stock -= quantity


@dataclass
class OrderItem:
    product_id: int
    quantity: int
    unit_price: Decimal
    id: Optional[int] = None
    order_id: Optional[int] = None


@dataclass
class Order:
    customer_name: str
    customer_email: str
    items: list[OrderItem] = field(default_factory=list)
    status: str = "pending"
    total_price: Decimal = Decimal("0")
    id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    def calculate_total(self) -> None:
        self.total_price = sum(i.unit_price * i.quantity for i in self.items)
