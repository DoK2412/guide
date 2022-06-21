from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from ..realization import output_database, new_entry, updating_data, delete_data
from ..models.operations import Addendum, Update, Delete


router = APIRouter(
    prefix='/operations',
)

token_auth_scheme = HTTPBearer()

@router.get('/')
async def reading_notebook():
    return {'status': 'Get запрос включен'}

@router.get('/entirebook')
async def entire_book(token: str = Depends(token_auth_scheme)):
    """
    Функция вывода всей записной книги
    :param token: токен пользователя
    :return: результат выполнения
    """
    base = await output_database(token)
    return base

@router.post('/entry')
async def entry_notebook(entry: Addendum, token: str = Depends(token_auth_scheme)):
    """
    Функция добавления нового аббонента
    :param entry: данные о аббоненте
    :param token: токен пользователя
    :return: результат выполнения
    """
    result = await new_entry(entry, token)
    return result

@router.post('/update')
async def update_notebook(update: Update, token: str = Depends(token_auth_scheme)):
    """
    Функция обновления аббонента
    :param update: данные обновления
    :param token: токен пользователя
    :return: результат выполнения
    """
    result = await updating_data(update, token)
    return result

@router.post('/delete')
async def delete_notebook(delete: Delete, token: str = Depends(token_auth_scheme)):
    """
    Функция удаления аббонента
    :param delete: данные аббонента
    :param token: токен пользователя
    :return: результат выполнения
    """
    result = await delete_data(delete, token)
    return result


