from typing import List
from pydantic import BaseModel
import datetime

from app.order_item.schemas import OrderItemDB, OrderItemCreate
from app.order.models import OrderStatus


class OrderBase(BaseModel):
    

    class Config:
        orm_mode = True


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class OrderDB(OrderBase):
    id: int
    created_at: datetime.datetime
    status: OrderStatus


class OrderOut(OrderBase):
    id: int
    created_at: datetime.datetime
    items: List[OrderItemDB]
    status: OrderStatus


class OrderStatusUpdate(OrderBase):
    status: OrderStatus
