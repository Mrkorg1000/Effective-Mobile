from typing import List
from fastapi import APIRouter, HTTPException, status
from app.product.dao import ProductDAO
from app.product.schemas import ProductCreate, ProductDB, ProductUpdate


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


# Получение списка товаров
@router.get("", response_model=List[ProductDB])
async def get_products():
    return await ProductDAO.find_all()


# Получение товара по id
@router.get("/{id}", response_model=ProductDB)
async def get_product(id: int):
    product = await ProductDAO.find_by_id(id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="product not found"
        )
    return product


# Создание товара
@router.post("", response_model=ProductDB, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate):
    new_product = await ProductDAO.add(product)
    return new_product


# Удаление товара
@router.delete("/{id}")
async def delete_product(id: int):
    product_to_delete = await ProductDAO.find_by_id(id)
    if not product_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="product not found"
        )
    await ProductDAO.delete(product_to_delete)
    return {"status": True, "message": "The product has been deleted"}


# Обновление информации о товаре
@router.patch("/{id}", response_model=ProductDB)
async def update_product(id: int, product_scheme: ProductUpdate):
    updated_product = await ProductDAO.update_object(id, product_scheme)

    return updated_product
