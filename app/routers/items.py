from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Item, Order
from app.schemas import ItemResponse, PurchaseResponse
from app.services.inventory_service import purchase_item_service


router = APIRouter()


@router.get("/items", response_model=list[ItemResponse])
async def get_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).order_by(Item.id))
    return result.scalars().all()


@router.post("/purchase/{item_id}", response_model=PurchaseResponse)
async def purchase_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await purchase_item_service(item_id=item_id, db=db)


@router.get("/orders/count")
async def order_count(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(func.count(Order.id)))

    return {
        "order_count": result.scalar()
    }