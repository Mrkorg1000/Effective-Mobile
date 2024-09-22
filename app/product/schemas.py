from decimal import Decimal
from typing import Optional
from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: str
    price: Decimal
    quantity: int

    class Config:
        orm_mode = True


class ProductCreate(ProductBase):
    pass


class ProductDB(ProductBase):
    id: int


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    quantity: Optional[int] = None
