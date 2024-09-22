from sqlalchemy import Column, String, Integer, Numeric
from app.database import Base
from sqlalchemy.orm import relationship
import uuid


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, )
    name = Column(String(200), unique=True, nullable=False)
    description = Column(String(1000), nullable=False)
    price = Column(Numeric(precision=10, scale=2), default=0)
    quantity = Column(Integer, default=0)

    order_items = relationship("OrderItem", back_populates="product")
