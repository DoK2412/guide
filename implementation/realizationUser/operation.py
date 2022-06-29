from fastapi import APIRouter, Depends, Response
from ..models.operations import Rreatings, Authorization, UserData
from .realizationsuser import registration, authorization
from ..database import Session, get_session


routerUser = APIRouter(
    prefix='/realizationUser'
)


@routerUser.post('/registration')
async def registration_user(subscriber: Rreatings, session: Session = Depends(get_session)):
    reg = await registration(subscriber, session)
    return reg


@routerUser.post('/authorizations', response_model=list[UserData])
async def authorization_user(user: Authorization, response: Response, session: Session = Depends(get_session)):
    entrance = await authorization(user, session, response)
    return entrance
