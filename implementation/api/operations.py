from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from ..database import get_session
from ..realization import output_database, new_entry, updating_data, delete_data
from ..models.operations import Addendum, Update, Withdrawalsubscribers


router = APIRouter(
    prefix='/operations',
)

@router.get('/')
async def reading_notebook():
    return {'status': 'Get запрос включен'}


@router.get('/entirebook', response_model=list[Withdrawalsubscribers])
async def entire_book(offset: int = 0, limit: int = Query(default=50, lte=50), session: Session = Depends(get_session)):
    """
    Функция вывода всей записной книги
    :param token: токен пользователя
    :return: результат выполнения
    """
    base = await output_database(offset, limit, session)
    return base

@router.post('/entry')
async def entry_notebook(entry: Addendum, session: Session = Depends(get_session)):
    """
    Функция добавления нового аббонента
    :param entry: данные о аббоненте
    :param token: токен пользователя
    :return: результат выполнения
    """
    result = await new_entry(entry, session)
    return result

@router.patch('/update/{user_id}')
async def update_notebook(user_id: int, user: Update, session: Session = Depends(get_session)):
    """
    Функция обновления аббонента
    :param update: данные обновления
    :param token: токен пользователя
    :return: результат выполнения
    """
    result = await updating_data(user_id, user, session)
    return result

@router.delete('/delete/{user_id}')
async def delete_notebook(user_id: int, session: Session = Depends(get_session)):
    """
    Функция удаления аббонента
    :param delete: данные аббонента
    :param token: токен пользователя
    :return: результат выполнения
    """
    result = await delete_data(user_id, session)
    return result


