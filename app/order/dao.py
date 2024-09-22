from app.dao.base import BaseDAO
from app.order.models import Order
from app.database import async_session_maker
from app.order.schemas import OrderCreate
from app.order_item.dao import OrderItemDAO
from app.order_item.models import OrderItem
from app.product.models import Product
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload


class OrderDAO(BaseDAO):
    model = Order

    @classmethod
    async def update_object(cls, object_id: int, object_update_scheme):
        async with async_session_maker() as session:
            object_upd = await session.get(cls.model, object_id)
            if not object_upd:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="object not found"
                )
            object_upd.status = object_update_scheme.status
            await session.commit()
            await session.refresh(object_upd)
            return object_upd

    @classmethod
    async def add(cls, object: OrderCreate):
        async with async_session_maker() as session:
            new_order = cls.model()
            session.add(new_order)
            await session.commit()
            await session.refresh(new_order)
            for item in object.items:
                product = await session.get(Product, item.product_id)
                if not product:
                    raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="object not found")
                if product.quantity < item.product_quantity:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Недостаточное количество товара {product.name}",
                    )
                product.quantity -= item.product_quantity
                new_order_item = OrderItem(
                    order_id=new_order.id,
                    product_id=item.product_id,
                    product_quantity=item.product_quantity,
                )

                session.add(new_order_item)
                await session.commit()
                await session.refresh(new_order_item)

            session.add(new_order)
            await session.commit()
            await session.refresh(new_order)
            return new_order

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .options(selectinload(cls.model.items))
                .filter_by(id=model_id)
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()
