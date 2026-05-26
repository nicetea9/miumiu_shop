from __future__ import annotations

from dataclasses import replace
from typing import Optional

from app.domain.entities import Category
from app.domain.exceptions import NotFoundError
from app.interfaces import AbstractCategoryRepository


class CategoryService:


    def __init__(self, repo: AbstractCategoryRepository):
        self._repo = repo

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Category]:
        return await self._repo.list(skip, limit)

    async def get_by_id(self, category_id: int) -> Category:
        category = await self._repo.get(category_id)
        if not category:
            raise NotFoundError("Категория", category_id)
        return category

    async def create(self, name: str, description: Optional[str] = None) -> Category:
        return await self._repo.save(Category(name=name, description=description))

    async def update(
        self,
        category_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Category:
        category = await self.get_by_id(category_id)
        updates = {k: v for k, v in {"name": name, "description": description}.items() if v is not None}
        updated = replace(category, **updates)
        return await self._repo.save(updated)

    async def delete(self, category_id: int) -> None:
        await self.get_by_id(category_id)  
        await self._repo.delete(category_id)
