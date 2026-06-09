import logging

from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Item, Order
from app.schemas import PurchaseResponse


logger = logging.getLogger(__name__)


async def purchase_item_service(
    item_id: int,
    db: AsyncSession,
) -> PurchaseResponse:
    logger.info("Purchase request received. item_id=%s", item_id)

    async with db.begin():
        stmt = (
            update(Item)
            .where(Item.id == item_id)
            .where(Item.stock > 0)
            .values(stock=Item.stock - 1)
            .returning(Item.id, Item.stock)
        )

        result = await db.execute(stmt)
        updated_item = result.first()

        if updated_item is None:
            logger.warning(
                "Purchase failed. item_id=%s reason=out_of_stock_or_not_found",
                item_id,
            )
            raise HTTPException(
                status_code=409,
                detail="Item does not exist or stock is not available.",
            )

        db.add(Order(item_id=item_id))

        logger.info(
            "Purchase successful. item_id=%s remaining_stock=%s",
            updated_item.id,
            updated_item.stock,
        )

        return PurchaseResponse(
            message="Purchase successful",
            item_id=updated_item.id,
            remaining_stock=updated_item.stock,
        )