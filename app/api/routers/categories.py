from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_category_service
from app.api.schemas import CategoryIn, CategoryOut, CategoryPatch
from app.use_cases import CategoryService

router = APIRouter(prefix="/categories", tags=["Категории"])


@router.get("/", response_model=list[CategoryOut])
async def list_categories(
    skip: int = 0, limit: int = 100, svc: CategoryService = Depends(get_category_service)
):
    return await svc.get_all(skip, limit)


@router.get("/{category_id}", response_model=CategoryOut)
async def get_category(category_id: int, svc: CategoryService = Depends(get_category_service)):
    return await svc.get_by_id(category_id)


@router.post("/", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
async def create_category(body: CategoryIn, svc: CategoryService = Depends(get_category_service)):
    return await svc.create(**body.model_dump())


@router.patch("/{category_id}", response_model=CategoryOut)
async def update_category(
    category_id: int, body: CategoryPatch, svc: CategoryService = Depends(get_category_service)
):
    return await svc.update(category_id, **body.model_dump(exclude_unset=True))


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, svc: CategoryService = Depends(get_category_service)):
    await svc.delete(category_id)
