from app.dao.base import BaseDAO
from app.product.models import Product


class ProductDAO(BaseDAO):
    model = Product
