from fastapi import  HTTPException, Depends
from sqlmodel import Field, Session, SQLModel, create_engine, select
from .models.operations import phonenumbers



async def output_database(offset: int, limit: int, session: Session):
    """
    Функция предназначена для вывода всего списка записной книги
    :param token: - данные из полученного заголовка
    :return: - список контактов либо ошибка
    """
    conclusion = session.exec(select(phonenumbers).offset(offset).limit(limit)).all()
    return conclusion


async def new_entry(entr, session: Session) -> dict:
    """
    Функция предназначена для добавления нового контакта
    :param entr:  данные о контакте
    :param token:  данные из полученного заголовка
    :return: возврат результата выполнения программы
    """
    db_app = phonenumbers.from_orm(entr)
    session.add(db_app)
    session.commit()
    session.refresh(db_app)
    return {'status': 200, 'massage': 'Number added to the'
                                          ' directory'}


async def updating_data(user_id, user , session: Session) -> dict:
    """
    Функция предназначена для обновления абонента
    :param update: новые значения абонента
    :param token:  данные из полученного заголовка
    :return: возврат результата выполнения функции
    """
    updating = session.get(phonenumbers, user_id)
    if not updating:
        raise HTTPException(status_code=404, detail="Hero not found")
    else:
        user_data = user.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(updating, key, value)
        session.add(updating)
        session.commit()
        session.refresh(updating)
        return {'status': 200, 'massage': 'Contact updated'}


async def delete_data(user_id, session: Session) -> dict:
    """
    Функция предназначена для удаления контакта из списка контактов
    :param delete: йд необходимого когтакта
    :param token:  данные из полученного заголовка
    :return: возврат результата выполнения функции
    """
    delet = session.get(phonenumbers, user_id)
    if not delet:
        raise HTTPException(status_code=404, detail="Hero not found")
    else:
        session.delete(delet)
        session.commit()
        return {'status': 200, 'massage': 'Contact deleted'}


