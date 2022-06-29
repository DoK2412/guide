from fastapi import HTTPException
from sqlmodel import Session, select
from .models.operations import phonenumbers, Record
from datetime import date



async def output_database(offset: int, limit: int, id_user: int, session: Session):
    """
    Функция предназначена для вывода всего списка записной книги
    :param token: - данные из полученного заголовка
    :return: - список контактов либо ошибка
    """
    conclusion = session.exec(select(phonenumbers).filter(phonenumbers.id_user == id_user, phonenumbers.removal == None).offset(offset).limit(limit)).all()
    return conclusion


async def new_entry(entr, id_user, session: Session) -> dict:

    """
    Функция предназначена для добавления нового контакта
    :param entr:  данные о контакте
    :param token:  данные из полученного заголовка
    :return: возврат результата выполнения программы
    """
    if entr.name.isalpha() and entr.numbers.isalnum():
        us = session.exec(select(phonenumbers).filter(id_user == phonenumbers.id_user, entr.name == phonenumbers.name)).all()
        if not us:
            record = Record()
            record.id_user = str(id_user)
            record.name = entr.name
            record.numbers = str(entr.numbers)

            db_app = phonenumbers.from_orm(record)
            session.add(db_app)
            session.commit()
            session.refresh(db_app)
            return {'status': 200, 'massage': 'Number added to the'
                                                  ' directory'}
        else:
            raise HTTPException(status_code=404, detail="Do you already have a contact with that name")
    else:
        raise HTTPException(status_code=404, detail="The number or name of the incorrect format")


async def updating_data(user_id, id_user, user, session: Session) -> dict:
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
        if updating.id_user == id_user:
            user_data = user.dict(exclude_unset=True)
            for key, value in user_data.items():
                setattr(updating, key, value)
            session.add(updating)
            session.commit()
            session.refresh(updating)
            return {'status': 200, 'massage': 'Contact updated'}
        else:
            raise HTTPException(status_code=404, detail="No access to the contact")


async def delete_data(user_id, id_user, session: Session) -> dict:
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
        if id_user == delet.id_user and delet.removal == None:
            delet.removal = date.today()
            session.commit()
            return {'status': 200, 'massage': 'Contact deleted'}
        else:
            raise HTTPException(status_code=404, detail="No access to the contact")


