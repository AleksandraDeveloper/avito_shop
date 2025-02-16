from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...database import get_db
from ...schemas import SendCoinRequest, ErrorResponse
from ..deps import get_current_user
from ...models import User, Transaction

router = APIRouter()

@router.post(
    "/api/sendCoin",
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def send_coin(
    transfer_data: SendCoinRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    to_user = db.query(User).filter(User.username == transfer_data.toUser).first()
    if not to_user:
        raise HTTPException(status_code=400, detail="Получатель не найден")
    if current_user.coins < transfer_data.amount:
        raise HTTPException(status_code=400, detail="Недостаточно монет")

    transaction = Transaction(
        from_user_id=current_user.id,
        to_user_id=to_user.id,
        amount=transfer_data.amount,
        transaction_type="TRANSFER"
    )

    current_user.coins -= transfer_data.amount
    to_user.coins += transfer_data.amount

    db.add(transaction)
    db.commit()

    return {}