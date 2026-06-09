import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import select, text

from app.database import AsyncSessionLocal
from app.models import Item
from app.routers.items import router as items_router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup started.")

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Item).where(Item.id == 1))
        existing_item = result.scalar_one_or_none()

        if existing_item is None:
            session.add(Item(id=1, name="PlayStation 5", stock=50))
            await session.commit()
            logger.info("Seed item created: PlayStation 5 with stock 50.")
        else:
            logger.info("Seed item already exists.")

    logger.info("Application startup completed.")

    yield

    logger.info("Application shutdown completed.")


app = FastAPI(
    title="High Concurrency Inventory System",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    return {"message": "Inventory API is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


app.include_router(items_router)