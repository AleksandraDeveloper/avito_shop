from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...database import get_db
from ...schemas import InfoResponse, ErrorResponse
from ..deps import get_current_user
from ...models import User

router = APIRouter()

@router.get(
    "/api/info",
    response_model=InfoResponse,
    responses={
        401: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def get_info(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db.refresh(current_user)
    inventory = [
        {"type": purchase.item.name, "quantity": purchase.quantity}
        for purchase in current_user.purchases
    ]
    received = [
        {"fromUser": t.from_user.username, "amount": t.amount}
        for t in current_user.received_transactions
    ]
    sent = [
        {"toUser": t.to_user.username, "amount": t.amount}
        for t in current_user.sent_transactions
    ]
    return {
        "coins": current_user.coins,
        "inventory": inventory,
        "coinHistory": {
            "received": received,
            "sent": sent
        }
    }