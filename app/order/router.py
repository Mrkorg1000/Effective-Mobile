from typing import List
from fastapi import APIRouter, HTTPException, status
from app.order.dao import OrderDAO
from app.order.schemas import OrderCreate, OrderDB, OrderOut, OrderStatusUpdate


router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


# Получение списка заказов
@router.get("", response_model=List[OrderDB])
async def get_orders():
    return await OrderDAO.find_all()


# Получение информации о заказе по id
@router.get("/{id}", response_model=OrderOut)
async def get_order(id: int):
    order = await OrderDAO.find_by_id(id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="order not found"
        )
    return order


# Обновление статуса заказа
@router.patch("/{id}/status", response_model=OrderDB)
async def update_order_status(id: int, update_scheme: OrderStatusUpdate):
    updated_order = await OrderDAO.update_object(id, update_scheme)
    return updated_order


# Создание заказа
@router.post("", response_model=OrderDB, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate):
    order = await OrderDAO.add(order)
    return order


