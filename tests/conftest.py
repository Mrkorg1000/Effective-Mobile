import pytest
import asyncio
import httpx
from app.config import settings
from app.database import Base
from app.product.models import Product
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import NullPool, select
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from httpx import AsyncClient
from main import app


DATABASE_URL_TEST = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"


engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)


async_session_maker_test = sessionmaker(
    bind=engine_test, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(autouse=True, scope="session") 
async def db() -> AsyncGenerator:
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker_test() as db:
        try:
            yield db
        finally:
            await db.close()


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def session():
    async with async_session_maker_test() as session:
        yield session


@pytest.fixture
async def test_product(session):
    test_pro = Product(
        name="My test product",
        description="Test product description",
        price=10.0,
        quantity=10
        )
    session.add(test_pro)
    await session.commit()
    await session.refresh(test_pro)
    return test_pro


def product_to_dict(product: Product):
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "quantity": product.quantity,
    }


async def get_objects_list(obj_cls, session):
    query = select(obj_cls)
    result = await session.execute(query)
    objects_list = result.scalars().all()
    return objects_list


async def get_object_id(obj_cls, session):
    query = select(obj_cls)
    result = await session.execute(query)
    object = result.scalar_one_or_none()
    if object:
        return str(object.id)


async def get_object(obj_cls, session):
    query = select(obj_cls)
    result = await session.execute(query)
    object = result.scalar_one_or_none()
    if object:
        return object
