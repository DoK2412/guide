from fastapi import APIRouter
from ..models.operations import Сreatings, Authorization
from .realizationsuser import registration, authorization, creating_token

routerUser = APIRouter(
    prefix='/realizationUser'
)


@routerUser.post('/registration')
async def registration_user(user: Сreatings):
    reg = await registration(user)
    return reg


@routerUser.post('/authorizations')
async def authorization_user(user: Authorization):
    entrance = await authorization(user)
    if entrance.get('id'):
        token = await creating_token(entrance)
        return token
    else:
        return entrance
