from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from app.domain.entities import Order, OrderItem
from app.domain.exceptions import InvalidStatusError, NotFoundError
from app.interfaces import AbstractOrderRepository, AbstractProductRepository


@dataclass
class OrderItemInput:
    product_id: int
    quantity: int


class OrderService:
    def __init__(
        self,
        order_repo: AbstractOrderRepository,
        product_repo: AbstractProductRepository,
    ):
        self._orders = order_repo
        self._products = product_repo

    async def get_all(self, skip: int = 0, limit: int = 50) -> list[Order]:
        return await self._orders.list(skip, limit)

    async def get_by_id(self, order_id: int) -> Order:
        order = await self._orders.get(order_id)
        if not order:
            raise NotFoundError("Заказ", order_id)
        return order

    async def create(
        self, customer_name: str, customer_email: str, items: list[OrderItemInput]
    ) -> Order:
        order_items: list[OrderItem] = []

        for item_input in items:
            product = await self._products.get(item_input.product_id)
            if not product:
                raise NotFoundError("Товар", item_input.product_id)

            product.reserve(item_input.quantity)
            await self._products.save(product)

            order_items.append(
                OrderItem(
                    product_id=product.id,
                    quantity=item_input.quantity,
                    unit_price=product.price,
                )
            )

        order = Order(
            customer_name=customer_name,
            customer_email=customer_email,
            items=order_items,
        )
        order.calculate_total()
        return await self._orders.save(order)

    async def update_status(self, order_id: int, status: str) -> Order:
        if status not in InvalidStatusError.ALLOWED:
            raise InvalidStatusError(status)
        order = await self.get_by_id(order_id)
        order.status = status
        return await self._orders.save(order)

    async def delete(self, order_id: int) -> None:
        await self.get_by_id(order_id)
        await self._orders.delete(order_id)
