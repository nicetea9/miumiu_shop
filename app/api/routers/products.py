from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import get_product_service
from app.api.schemas import ProductIn, ProductOut, ProductPatch
from app.use_cases import ProductService

router = APIRouter(prefix="/products", tags=["Товары"])


@router.get("/", response_model=list[ProductOut])
async def list_products(
    skip: int = 0,
    limit: int = 20,
    category_id: Optional[int] = Query(None),
    available_only: bool = Query(False),
    svc: ProductService = Depends(get_product_service),
):
    return await svc.get_all(skip, limit, category_id, available_only)


@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: int, svc: ProductService = Depends(get_product_service)):
    return await svc.get_by_id(product_id)


@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(body: ProductIn, svc: ProductService = Depends(get_product_service)):
    return await svc.create(**body.model_dump())


@router.patch("/{product_id}", response_model=ProductOut)
async def update_product(
    product_id: int, body: ProductPatch, svc: ProductService = Depends(get_product_service)
):
    return await svc.update(product_id, **body.model_dump(exclude_unset=True))


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, svc: ProductService = Depends(get_product_service)):
    await svc.delete(product_id)
