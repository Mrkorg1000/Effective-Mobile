from sqlalchemy import DateTime, Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base
from enum import Enum, unique
import datetime


@unique
class OrderStatus(str,Enum):
    IN_PROGRESS = "в процессе"
    SHIPPED = "отправлен"
    DELIVERED = "доставлен"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    created_at = Column(
        DateTime, default=lambda: datetime.datetime.now(), nullable=False
    )
    status = Column(String, default=OrderStatus.IN_PROGRESS)

    items = relationship("OrderItem", back_populates="order")
