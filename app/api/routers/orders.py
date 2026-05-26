from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_order_service
from app.api.schemas import OrderIn, OrderOut, OrderStatusIn
from app.use_cases import OrderItemInput, OrderService

router = APIRouter(prefix="/orders", tags=["Заказы"])


@router.get("/", response_model=list[OrderOut])
async def list_orders(skip: int = 0, limit: int = 50, svc: OrderService = Depends(get_order_service)):
    return await svc.get_all(skip, limit)


@router.get("/{order_id}", response_model=OrderOut)
async def get_order(order_id: int, svc: OrderService = Depends(get_order_service)):
    return await svc.get_by_id(order_id)


@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create_order(body: OrderIn, svc: OrderService = Depends(get_order_service)):
    items = [OrderItemInput(product_id=i.product_id, quantity=i.quantity) for i in body.items]
    return await svc.create(body.customer_name, body.customer_email, items)


@router.patch("/{order_id}/status", response_model=OrderOut)
async def update_status(
    order_id: int, body: OrderStatusIn, svc: OrderService = Depends(get_order_service)
):
    return await svc.update_status(order_id, body.status)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: int, svc: OrderService = Depends(get_order_service)):
    await svc.delete(order_id)
