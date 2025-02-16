from fastapi import APIRouter
from .auth import router as auth_router
from .info import router as info_router
from .purchase import router as purchase_router
from .transaction import router as transfer_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(info_router)
router.include_router(purchase_router)
router.include_router(transfer_router)