from fastapi import HTTPException
from sqlmodel import Session, select
from ..models.operations import users
from passlib.context import CryptContext # хеширование паролей


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


async def authorization(subscriber, session: Session) -> dict:
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
        # кодирование пароля
        password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        # проверка с хранящимся в базе
        if password_context.verify(subscriber.password,
                                   contact[0].password):
            return contact
        else:
            raise HTTPException(status_code=403, detail="Username or password is not correct")



