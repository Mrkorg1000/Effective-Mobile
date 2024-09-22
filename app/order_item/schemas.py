from pydantic import BaseModel


class OrderItemBase(BaseModel):
    product_id: int
    product_quantity: int

    class Config:
        orm_mode = True


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemDB(OrderItemBase):
    id: int
    order_id: int
