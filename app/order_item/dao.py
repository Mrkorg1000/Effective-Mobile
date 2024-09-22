from app.dao.base import BaseDAO
from app.order_item.models import OrderItem


class OrderItemDAO(BaseDAO):
    model = OrderItem
