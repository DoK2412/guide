import datetime
import jwt

from .settings import setting

from implementation.tables import Quide
from .database import Session


async def token_processing(token) -> dict:
    """
    Функция предназначена для проверки валидности токена
    :param token: - данные из полученного заголовка
    :return: - сформированные словарь с данными пользователя либо ошидку
    """
    try:
        transformation_token = token.json().split()
        data_user = jwt.decode(transformation_token[3][1:-2], setting.sekret,
                               algorithms=['HS256', ])
        return data_user
    except:
        return {'status': 403, 'massage': 'The token is not valid'}


async def output_database(token) -> dict:
    """
    Функция предназначена для вывода всего списка записной книги
    :param token: - данные из полученного заголовка
    :return: - список контактов либо ошибка
    """
    valid_token = await token_processing(token)
    if valid_token.get('id'):
        ssession = Session()
        response = ssession.query(Quide).all()
        return response
    else:
        return valid_token


async def new_entry(entr, token) -> dict:
    """
    Функция предназначена для добавления нового контакта
    :param entr:  данные о контакте
    :param token:  данные из полученного заголовка
    :return: возврат результата выполнения программы
    """
    valid_token =  await token_processing(token)
    if valid_token.get('id'):
        if entr.name.isalpha() and entr.tel.isdigit():
            current_date = datetime.datetime.now()
            ssession = Session()
            user = Quide(
                id_user=valid_token['id'],
                name=entr.name.lower(),
                numbers=entr.tel,
                date=current_date,
                update=current_date
            )
            ssession.add(user)
            ssession.commit()
            return {'status': 200, 'massage': 'Number added to the'
                                              ' directory'}
        else:
            return {'status': 403, 'massage': 'The name or number does '
                                              'not meet the standard'}
    else:
        return valid_token


async def updating_data(update, token) -> dict:
    """
    Функция предназначена для обновления абонента
    :param update: новые значения абонента
    :param token:  данные из полученного заголовка
    :return: возврат результата выполнения функции
    """
    valid_token = await token_processing(token)
    if valid_token.get('id'):
        current_date = datetime.datetime.now()
        ssession = Session()

        if update.name and update.tel:
            if update.name.isalpha() and update.tel.isdigit():
                ssession.query(Quide).filter(Quide.id == update.id).update(
                    {'name': update.name, 'numbers': update.tel,
                     'update': current_date})
                ssession.commit()
                return {'status': 200, 'massage': 'All user data updated'}
            else:
                return {'status': 403, 'massage': 'The name or number does'
                                                  ' not meet the standard'}
        elif update.name is None and update.tel:
            if update.tel.isdigit():
                ssession.query(Quide).filter(Quide.id == update.id).update(
                    {'numbers': update.tel, 'update': current_date})
                ssession.commit()
                return {'status': 200, 'massage': 'Contact number updated'}
            else:
                return {'status': 403, 'massage': 'The phone number does'
                                                  ' not meet the standard'}
        elif update.name and update.tel is None:
            if update.name.isalpha():
                ssession.query(Quide).filter(Quide.id == update.id).update(
                    {'name': update.name, 'update': current_date})
                ssession.commit()
                return {'status': 200, 'massage': 'Subscriber name updated'}
            else:
                return {'status': 403, 'massage': 'The name does not'
                                                  ' match the standard'}
    else:
        return valid_token


async def delete_data(delete, token) -> dict:
    """
    Функция предназначена для удаления контакта из списка контактов
    :param delete: йд необходимого когтакта
    :param token:  данные из полученного заголовка
    :return: возврат результата выполнения функции
    """
    valid_token = await token_processing(token)
    if valid_token.get('id'):
        ssession = Session()
        user = ssession.query(Quide).filter(Quide.id == delete.id).first()
        if user:
            ssession.delete(user)
            ssession.commit()
            return {'status': 200, 'massage': 'Contact deleted'}
        else:
            return {'status': 200, 'massage': 'The contact is'
                                              ' not in the database'}
    else:
        return valid_token
