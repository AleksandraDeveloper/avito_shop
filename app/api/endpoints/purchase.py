from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...database import get_db
from ...schemas.common import ErrorResponse
from ..deps import get_current_user
from ...models import User, Item, Purchase

router = APIRouter()

@router.get(
    "/api/buy/{item}",
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def buy_item(
    item: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_item = db.query(Item).filter(Item.name == item).first()
    if not db_item:
        raise HTTPException(status_code=400, detail="Товар не найден")
    if current_user.coins < db_item.price:
        raise HTTPException(status_code=400, detail="Недостаточно монет")

    purchase = Purchase(user_id=current_user.id, item_id=db_item.id, quantity=1)
    current_user.coins -= db_item.price
    
    db.add(purchase)
    db.commit()
    
    return {}