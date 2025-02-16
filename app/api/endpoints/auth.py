from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...database import get_db
from ...schemas import AuthRequest, AuthResponse, ErrorResponse
from ...core.security import create_token, get_password, verify_password
from ...models import User

router = APIRouter()

@router.post(
    "/api/auth",
    response_model=AuthResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def login(auth_data: AuthRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == auth_data.username).first()
    if not user:
        user = User(
            username=auth_data.username,
            password=get_password(auth_data.password)
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    elif not verify_password(auth_data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Неверный пароль"
        )
    
    token = create_token(data={"sub": user.username})
    return {"token": token}