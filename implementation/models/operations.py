from sqlmodel import Field, SQLModel
from typing import List, Optional
from datetime import date

#  таблица номеров
class phonenumbers(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str
    numbers: str
    date = date.today()
    update = date.today()


# добавление пользователя
class Addendum(SQLModel):
    name: str
    numbers: str

# вывод списка обонентов
class Withdrawalsubscribers(Addendum):
    id: int


# обновление контакта
class Update(SQLModel):
    name: Optional[str] = None
    numbers: Optional[str] = None
    update = date.today()

# таблица пользователей
class users(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str
    password: str
    date = date.today()


# регистрация пользователя
class Rreatings(SQLModel):
    name: str
    password: str


# вход пользователя
class Authorization(SQLModel):
    name: str
    password: str


# вывод данных о пользователе
class UserData(SQLModel):
    id: int
    name: str





