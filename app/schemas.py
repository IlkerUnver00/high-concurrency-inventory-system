from datetime import datetime
from pydantic import BaseModel


class ItemResponse(BaseModel):
    id: int
    name: str
    stock: int

    model_config = {
        "from_attributes": True
    }


class PurchaseResponse(BaseModel):
    message: str
    item_id: int
    remaining_stock: int


class OrderResponse(BaseModel):
    id: int
    item_id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }