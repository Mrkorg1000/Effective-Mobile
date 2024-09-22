from fastapi import FastAPI
from app.database import Base, engine
from app.product.router import router as router_product
from app.order.router import router as router_order


app = FastAPI()


app.include_router(router_product)
app.include_router(router_order)


@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
