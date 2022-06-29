import jwt


from ..settings import setting
from fastapi import HTTPException, Response
from sqlmodel import Session, select
from ..models.operations import users
from passlib.context import CryptContext # хеширование паролей
from ..realizationUser.sessionuser import save_token


async def jwt_toron(contact):
    data = {'id': contact[0].id, 'name': contact[0].name}
    tokens = jwt.encode(payload=data, key=setting.sekret)
    return tokens


async def registration(subscriber, session: Session) -> dict:
    """
    Функция предназначена для регистрации пользователя в приложении
    производит проверку корректности данных, хеширует пароль и
    записывает пользователя в базу данных
    :param user: - логин и пароль пользователя
    :return: - возвращает словарь с результатом выполнения функции
    """
    contact = session.exec(select(users).filter(users.name == subscriber.name)).all()
    if contact:
        raise HTTPException(status_code=403, detail="The contact was found in the database")
    elif not contact and (subscriber.name.isalpha() and subscriber.password.isdigit()):
        # кодирование пароля
        password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        subscriber.password = password_context.hash(subscriber.password)
        subscriber.name = subscriber.name.lower()
        reg_subscriber = users.from_orm(subscriber)
        session.add(reg_subscriber)
        session.commit()
        session.refresh(reg_subscriber)
        return {'status': 200, 'massage': 'The user has been'
                                          ' added to the database'}
    else:
        raise HTTPException(status_code=404, detail="The user is in the database or the name and password do not meet the standard")


async def authorization(subscriber, session: Session, response: Response) -> dict:
    """
    Функция предназначена для входа пользователя в приложение с последующей
    его аудентификацией в нем.
    :param user: данные о пользователе
    :return: возвращает словарь с пользовательским id и именем либо данными
    об ошибке
    """
    contact = session.exec(select(users).filter(users.name == subscriber.name)).all()
    if not contact:
        raise HTTPException(status_code=403, detail="The user is not in the database")
    else:

        password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        # проверка с хранящимся в базе
        if password_context.verify(subscriber.password,
                                   contact[0].password):
            token = await jwt_toron(contact)
            await save_token(token, session)
            response.set_cookie(key='token', value=token, httponly=True)
            return contact
        else:
            raise HTTPException(status_code=403, detail="Username or password is not correct")



