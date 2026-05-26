"""
DI-контейнер: связывает инфраструктуру с use cases.
FastAPI-зависимости живут только здесь — роутеры про SQLAlchemy не знают.
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.session import get_db
from app.infrastructure.repositories import CategoryRepository, OrderRepository, ProductRepository
from app.use_cases import CategoryService, OrderService, ProductService


def get_category_service(db: AsyncSession = Depends(get_db)) -> CategoryService:
    return CategoryService(CategoryRepository(db))


def get_product_service(db: AsyncSession = Depends(get_db)) -> ProductService:
    return ProductService(ProductRepository(db))


def get_order_service(db: AsyncSession = Depends(get_db)) -> OrderService:
    return OrderService(OrderRepository(db), ProductRepository(db))
