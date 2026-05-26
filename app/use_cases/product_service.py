from __future__ import annotations

from dataclasses import replace
from decimal import Decimal
from typing import Optional

from app.domain.entities import Product
from app.domain.exceptions import NotFoundError
from app.interfaces import AbstractProductRepository


class ProductService:
    def __init__(self, repo: AbstractProductRepository):
        self._repo = repo

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 20,
        category_id: Optional[int] = None,
        available_only: bool = False,
    ) -> list[Product]:
        if category_id is not None:
            return await self._repo.list_by_category(category_id, skip, limit)
        if available_only:
            return await self._repo.list_available(skip, limit)
        return await self._repo.list(skip, limit)

    async def get_by_id(self, product_id: int) -> Product:
        product = await self._repo.get(product_id)
        if not product:
            raise NotFoundError("Товар", product_id)
        return product

    async def create(
        self,
        name: str,
        price: Decimal,
        stock: int = 0,
        is_available: bool = True,
        description: Optional[str] = None,
        category_id: Optional[int] = None,
    ) -> Product:
        return await self._repo.save(
            Product(
                name=name,
                price=price,
                stock=stock,
                is_available=is_available,
                description=description,
                category_id=category_id,
            )
        )

    async def update(self, product_id: int, **kwargs) -> Product:
        product = await self.get_by_id(product_id)
        updates = {k: v for k, v in kwargs.items() if v is not None}
        updated = replace(product, **updates)
        return await self._repo.save(updated)

    async def delete(self, product_id: int) -> None:
        await self.get_by_id(product_id)
        await self._repo.delete(product_id)
