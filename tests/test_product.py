from app.product.models import Product
from conftest import get_objects_list, product_to_dict, get_object_id, get_object


router = "/products"
router_id = "/products/{id}"


# Тестовый сценарий: Исходное состояние -> БД пустая.
# 1. Вывод пустого списка продуктов.
# 2. Создание продукта.
# 3. Вывод списка продуктов.
# 4. Получение продукта по id.
# 5. Получение продукта по несуществующему id.
# 6. Изменеие продукта
# 7. Удаление продукта.


async def test_get_empty_product_list(ac, session):
    resp = await ac.get(router, follow_redirects=True)
    product_list = await get_objects_list(Product, session)
    assert resp.status_code == 200
    assert resp.json() == product_list


async def test_create_product(ac, session):
    resp = await ac.post(
        router,
        json={
            "name": "My test product",
            "description": "Test product description",
            "price": 10.0,
            "quantity": 10,
        },
        follow_redirects=True,
    )
    assert resp.status_code == 201
    product_id = resp.json()["id"]
    product = await session.get(Product, product_id)
    assert resp.json() == product_to_dict(product)


async def test_get_product_list(ac, session):
    resp = await ac.get(router, follow_redirects=True)
    product_list = await get_objects_list(Product, session)
    assert resp.status_code == 200
    assert resp.json() == [product_to_dict(product) for product in product_list]


async def test_get_product_by_id(ac, session):
    product_id = await get_object_id(Product, session)

    resp = await ac.get(
        router_id.format(id=product_id),
    )
    product = await get_object(Product, session)
    assert resp.status_code == 200
    assert resp.json() == product_to_dict(product)


async def test_product_not_found(ac):
    resp = await ac.get(
        router_id.format(id=77),
    )
    assert resp.status_code == 404
    assert resp.json() == {"detail": "product not found"}


async def test_update_product(ac, session):
    product_id = await get_object_id(Product, session)

    resp = await ac.patch(
        router_id.format(id=product_id),
        json={
            "name": "My updated product",
            "description": "My updated product description",
        },
    )
    updated_product = await get_object(Product, session)

    assert resp.status_code == 200
    assert resp.json()["name"] == updated_product.name
    assert resp.json()["description"] == updated_product.description


async def test_delete_product(ac, session):
    product_id = await get_object_id(Product, session)

    resp = await ac.delete(
        router_id.format(id=product_id),
    )
    assert resp.status_code == 200
    assert resp.json() == {
        "status": True,
        "message": "The product has been deleted",
    }
