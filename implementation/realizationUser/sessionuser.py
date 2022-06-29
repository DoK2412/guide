from ..database import get_session
from ..models.operations import tokens, App_token
from fastapi import Depends, HTTPException
from sqlmodel import Session, select


async def save_token(token_on, session):
    """Функция добавления токена"""
    try:
        App_token.tokens = token_on
        bd_app = tokens.from_orm(App_token)
        session.add(bd_app)
        session.commit()
        session.refresh(bd_app)
    except:
        raise HTTPException(status_code=404, detail="Writing the token to the database failed")


async def overwriting_token(token_on, session: Session = Depends(get_session)):
    """Функуия проверки токена"""
    toren = session.exec(select(tokens).filter(token_on == tokens.tokens)).all()
    if not toren:
        return None
    else:
        return True
