import asyncio

import httpx
import pytest
from sqlalchemy import delete, func, select, update

from app.database import AsyncSessionLocal
from app.models import Item, Order


BASE_URL = "http://127.0.0.1:8000"
ITEM_ID = 1
INITIAL_STOCK = 100
REQUEST_COUNT = 500


async def reset_database():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            await session.execute(delete(Order))
            await session.execute(
                update(Item)
                .where(Item.id == ITEM_ID)
                .values(stock=INITIAL_STOCK)
            )


async def get_final_state():
    async with AsyncSessionLocal() as session:
        stock_result = await session.execute(
            select(Item.stock).where(Item.id == ITEM_ID)
        )
        order_count_result = await session.execute(
            select(func.count(Order.id))
        )

        return {
            "stock": stock_result.scalar_one(),
            "order_count": order_count_result.scalar_one(),
        }


async def send_purchase_request(client: httpx.AsyncClient):
    response = await client.post(
        f"{BASE_URL}/purchase/{ITEM_ID}"
    )
    return response.status_code


@pytest.mark.asyncio
async def test_high_concurrency_purchase():
    await reset_database()

    async with httpx.AsyncClient(timeout=30.0) as client:
        tasks = [
            send_purchase_request(client)
            for _ in range(REQUEST_COUNT)
        ]

        status_codes = await asyncio.gather(*tasks)

    success_count = status_codes.count(200)
    failed_count = status_codes.count(409)

    final_state = await get_final_state()

    assert success_count == INITIAL_STOCK
    assert failed_count == REQUEST_COUNT - INITIAL_STOCK
    assert final_state["stock"] == 0
    assert final_state["order_count"] == INITIAL_STOCK