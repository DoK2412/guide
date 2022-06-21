from fastapi import APIRouter
from .operation import routerUser as routerUsers


router = APIRouter()
router.include_router(routerUsers)
