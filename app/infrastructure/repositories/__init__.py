"""
Конкретные реализации репозиториев через SQLAlchemy.

DRY: маппер ORM ↔ domain-entity вынесен в отдельные функции,
     не дублируется в каждом методе.
"""

from __future__ import annotations


from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.entities import Category, Order, OrderItem, Product
from app.infrastructure.db.models import CategoryORM, OrderItemORM, OrderORM, ProductORM
from app.interfaces import (
    AbstractCategoryRepository,
    AbstractOrderRepository,
    AbstractProductRepository,
)


# ── Mappers  ──────────────────────────

def _to_category(row: CategoryORM) -> Category:
    return Category(id=row.id, name=row.name, description=row.description, created_at=row.created_at)


def _to_product(row: ProductORM) -> Product:
    return Product(
        id=row.id, name=row.name, description=row.description,
        price=row.price, stock=row.stock, is_available=row.is_available,
        category_id=row.category_id, created_at=row.created_at, updated_at=row.updated_at,
    )


def _to_order(row: OrderORM) -> Order:
    return Order(
        id=row.id, customer_name=row.customer_name, customer_email=row.customer_email,
        status=row.status, total_price=row.total_price, created_at=row.created_at,
        items=[
            OrderItem(
                id=i.id, order_id=i.order_id, product_id=i.product_id,
                quantity=i.quantity, unit_price=i.unit_price,
            )
            for i in row.items
        ],
    )


# ── Category ──────────────────────────────────────────────────────────────────

class CategoryRepository(AbstractCategoryRepository):
    def __init__(self, db: AsyncSession):
        self._db = db

    async def get(self, entity_id: int) -> Optional[Category]:
        row = await self._db.get(CategoryORM, entity_id)
        return _to_category(row) if row else None

    async def list(self, skip: int, limit: int) -> list[Category]:
        result = await self._db.execute(select(CategoryORM).offset(skip).limit(limit))
        return [_to_category(r) for r in result.scalars().all()]

    async def save(self, entity: Category) -> Category:
        if entity.id:
            row = await self._db.get(CategoryORM, entity.id)
            row.name = entity.name
            row.description = entity.description
        else:
            row = CategoryORM(name=entity.name, description=entity.description)
            self._db.add(row)
        await self._db.commit()
        await self._db.refresh(row)
        return _to_category(row)

    async def delete(self, entity_id: int) -> None:
        row = await self._db.get(CategoryORM, entity_id)
        if row:
            await self._db.delete(row)
            await self._db.commit()


# ── Product ───────────────────────────────────────────────────────────────────

class ProductRepository(AbstractProductRepository):
    def __init__(self, db: AsyncSession):
        self._db = db

    async def get(self, entity_id: int) -> Optional[Product]:
        row = await self._db.get(ProductORM, entity_id)
        return _to_product(row) if row else None

    async def list(self, skip: int, limit: int) -> list[Product]:
        result = await self._db.execute(select(ProductORM).offset(skip).limit(limit))
        return [_to_product(r) for r in result.scalars().all()]

    async def list_by_category(self, category_id: int, skip: int, limit: int) -> list[Product]:
        result = await self._db.execute(
            select(ProductORM).where(ProductORM.category_id == category_id).offset(skip).limit(limit)
        )
        return [_to_product(r) for r in result.scalars().all()]

    async def list_available(self, skip: int, limit: int) -> list[Product]:
        result = await self._db.execute(
            select(ProductORM)
            .where(ProductORM.is_available == True, ProductORM.stock > 0)
            .offset(skip).limit(limit)
        )
        return [_to_product(r) for r in result.scalars().all()]

    async def save(self, entity: Product) -> Product:
        if entity.id:
            row = await self._db.get(ProductORM, entity.id)
            for attr in ("name", "description", "price", "stock", "is_available", "category_id"):
                setattr(row, attr, getattr(entity, attr))
        else:
            row = ProductORM(
                name=entity.name, description=entity.description, price=entity.price,
                stock=entity.stock, is_available=entity.is_available, category_id=entity.category_id,
            )
            self._db.add(row)
        await self._db.commit()
        await self._db.refresh(row)
        return _to_product(row)

    async def delete(self, entity_id: int) -> None:
        row = await self._db.get(ProductORM, entity_id)
        if row:
            await self._db.delete(row)
            await self._db.commit()


# ── Order ─────────────────────────────────────────────────────────────────────

class OrderRepository(AbstractOrderRepository):
    def __init__(self, db: AsyncSession):
        self._db = db

    async def get(self, entity_id: int) -> Optional[Order]:
        result = await self._db.execute(
            select(OrderORM).options(selectinload(OrderORM.items)).where(OrderORM.id == entity_id)
        )
        row = result.scalar_one_or_none()
        return _to_order(row) if row else None

    async def list(self, skip: int, limit: int) -> list[Order]:
        result = await self._db.execute(
            select(OrderORM).options(selectinload(OrderORM.items)).offset(skip).limit(limit)
        )
        return [_to_order(r) for r in result.scalars().all()]

    async def save(self, entity: Order) -> Order:
        if entity.id:
            row = await self._db.execute(
                select(OrderORM).options(selectinload(OrderORM.items)).where(OrderORM.id == entity.id)
            )
            row = row.scalar_one()
            row.status = entity.status
            row.total_price = entity.total_price
        else:
            row = OrderORM(
                customer_name=entity.customer_name,
                customer_email=entity.customer_email,
                status=entity.status,
                total_price=entity.total_price,
                items=[
                    OrderItemORM(product_id=i.product_id, quantity=i.quantity, unit_price=i.unit_price)
                    for i in entity.items
                ],
            )
            self._db.add(row)
        await self._db.commit()
        result = await self._db.execute(
            select(OrderORM).options(selectinload(OrderORM.items)).where(OrderORM.id == row.id)
        )
        return _to_order(result.scalar_one())

    async def delete(self, entity_id: int) -> None:
        row = await self._db.get(OrderORM, entity_id)
        if row:
            await self._db.delete(row)
            await self._db.commit()
