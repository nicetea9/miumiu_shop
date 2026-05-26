from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


# ── Category

class CategoryIn(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None


class CategoryPatch(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None


class CategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: Optional[str]
    created_at: datetime


# ── Product
class ProductIn(BaseModel):
    name: str = Field(..., max_length=200)
    price: Decimal = Field(..., gt=0)
    stock: int = Field(0, ge=0)
    is_available: bool = True
    description: Optional[str] = None
    category_id: Optional[int] = None


class ProductPatch(BaseModel):
    name: Optional[str] = Field(None, max_length=200)
    price: Optional[Decimal] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    is_available: Optional[bool] = None
    description: Optional[str] = None
    category_id: Optional[int] = None


class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    price: Decimal
    stock: int
    is_available: bool
    description: Optional[str]
    category_id: Optional[int]
    created_at: datetime


# ── Order

class OrderItemIn(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)


class OrderItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int]
    product_id: int
    quantity: int
    unit_price: Decimal


class OrderIn(BaseModel):
    customer_name: str = Field(..., max_length=200)
    customer_email: str
    items: list[OrderItemIn] = Field(..., min_length=1)

    @field_validator("customer_email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Email must contain @")
        return v


class OrderStatusIn(BaseModel):
    status: str


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    customer_name: str
    customer_email: str
    status: str
    total_price: Decimal
    created_at: datetime
    items: list[OrderItemOut] = []
