import datetime
import jwt


from implementation.tables import User
from ..database import Session
from ..settings import setting
from passlib.context import CryptContext # хеширование паролей


async def registration(user) -> dict:
    """
    Функция предназначена для регистрации пользователя в приложении
    производит проверку корректности данных, хеширует пароль и
    записывает пользователя в базу данных
    :param user: - логин и пароль пользователя
    :return: - возвращает словарь с результатом выполнения функции
    """
    session = Session()
    users = session.query(User).filter(User.name == user.name).first()

    if users is None and (user.name.isalpha() and user.password.isdigit()):
        current_date = datetime.datetime.now()
        # кодирование пароля
        password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        code_key = password_context.hash(user.password)

        user_app = User(
            name=user.name.lower(),
            password=code_key,
            date=current_date,
        )
        session.add(user_app)
        session.commit()
        return {'status': 200, 'massage': 'The user has been'
                                          ' added to the database'}
    else:
        return {'status': 403, 'massage': 'The user is in the database or the'
                                          ' name and password do not meet the'
                                          ' standard'}


async def authorization(user) -> dict:
    """
    Функция предназначена для входа пользователя в приложение с последующей
    его аудентификацией в нем.
    :param user: данные о пользователе
    :return: возвращает словарь с пользовательским id и именем либо данными
    об ошибке
    """
    session = Session()
    users = session.query(User).filter(User.name == user.name).first()
    if users:
        data_processing = vars(users)
        # кодирование пароля
        password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        # проверка с хранящимся в базе
        if password_context.verify(user.password,
                                   data_processing['password']):
            return {'id': data_processing['id'],
                    'name': data_processing['name']}
        else:
            return {'status': 403, 'massage': 'The user is in the database or'
                                              ' the name and password do not'
                                              ' meet the standard'}


async def creating_token(user):
    """
    Функция предназнчена для создания токена для пользователя
    :param user: данные о пользователе для преобразования в токен
    :return: возвращает сформированный токен
    """
    tokens = jwt.encode(payload=user, key=setting.sekret)
    return tokens


