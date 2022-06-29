import jwt


from ..settings import setting
from typing import Optional

from fastapi import APIRouter, Depends, Query, Cookie, HTTPException, Response
from sqlmodel import Session
from ..database import get_session
from ..realization import output_database, new_entry, updating_data, delete_data
from ..models.operations import Addendum, Update, Withdrawalsubscribers
from ..realizationUser.sessionuser import overwriting_token

router = APIRouter(
    prefix='/operations',
)


@router.get('/')
async def reading_notebook():
    return {'status': 'Get запрос включен'}


async def decryptions(token):
    """Функция раскодирования токена"""
    data_user = jwt.decode(token, setting.sekret,
                                       algorithms=['HS256', ])
    return data_user['id']


async def decod(token, session):
    """
    Функция предназначена для проверки доступа переданных из куки
    :param token: данные полученные из куки
    :return: возвращаем bool значения о доступе к работе
    """
    db_token = await overwriting_token(token, session)
    if db_token:
        user_id = await decryptions(token)
        return user_id
    else:
        raise HTTPException(status_code=403, detail="The token is not valid")


@router.get('/entirebook', response_model=list[Withdrawalsubscribers])
async def entire_book(offset: int = 0,
                      token: Optional[str] = Cookie(None),
                      limit: int = Query(default=50, lte=50),
                      session: Session = Depends(get_session)):
    """
    Функция вывода всей записной книги
    :param token: токен пользователя
    :return: результат выполнения
    """
    id_user = await decod(token, session)
    if id_user:
        base = await output_database(offset, limit, id_user, session)
        return base
    else:
        raise HTTPException(status_code=403, detail="Access denied")


@router.post('/entry')
async def entry_notebook(entry: Addendum,
                         token: Optional[str] = Cookie(None),
                         session: Session = Depends(get_session)):
    """
    Функция добавления нового аббонента
    :param entry: данные о аббоненте
    :param token: токен пользователя
    :return: результат выполнения
    """

    id_user = await decod(token, session)
    if id_user:
        result = await new_entry(entry, id_user, session)
        return result
    else:
        raise HTTPException(status_code=403, detail="Access denied")


@router.patch('/update/{user_id}')
async def update_notebook(user_id: int,
                          user: Update,
                          session: Session = Depends(get_session),
                          token: Optional[str] = Cookie(None)):
    """
    Функция обновления аббонента
    :param update: данные обновления
    :param token: токен пользователя
    :return: результат выполнения
    """
    id_user = await decod(token, session)
    if id_user:
        result = await updating_data(user_id, id_user, user, session)
        return result
    else:
        raise HTTPException(status_code=403, detail="Access denied")


@router.delete('/delete/{user_id}')
async def delete_notebook(user_id: int,
                          session: Session = Depends(get_session),
                          token: Optional[str] = Cookie(None),):
    """
    Функция удаления аббонента
    :param delete: данные аббонента
    :param token: токен пользователя
    :return: результат выполнения
    """
    id_user = await decod(token, session)
    if id_user:
        result = await delete_data(user_id, id_user, session)
        return result
    else:
        raise HTTPException(status_code=403, detail="Access denied")


