from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

from app.domain.entities import Category, Order, Product

T = TypeVar("T")


class AbstractRepository(ABC, Generic[T]):
 

    @abstractmethod
    async def get(self, entity_id: int) -> Optional[T]: ...

    @abstractmethod
    async def list(self, skip: int, limit: int) -> list[T]: ...

    @abstractmethod
    async def save(self, entity: T) -> T: ...

    @abstractmethod
    async def delete(self, entity_id: int) -> None: ...


class AbstractCategoryRepository(AbstractRepository[Category]):
    pass


class AbstractProductRepository(AbstractRepository[Product]):
    @abstractmethod
    async def list_by_category(
        self, category_id: int, skip: int, limit: int
    ) -> list[Product]: ...

    @abstractmethod
    async def list_available(self, skip: int, limit: int) -> list[Product]: ...


class AbstractOrderRepository(AbstractRepository[Order]):
    pass
