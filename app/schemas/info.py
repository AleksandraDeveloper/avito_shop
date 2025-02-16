from pydantic import BaseModel, ConfigDict
from typing import List

class InventoryItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    quantity: int

class ReceivedCoin(BaseModel):
    fromUser: str
    amount: int

class SentCoin(BaseModel):
    toUser: str
    amount: int

class CoinHistory(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    amount: int
    type: str
    with_user: str

class InfoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    coins: int
    inventory: List[InventoryItem]
    history: List[CoinHistory]