from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from typing import List, Optional, Union
from datetime import date
import datetime


#  таблица номеров
class phonenumbers(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    id_user: int
    name: str
    numbers: str
    date = date.today()
    update = date.today()
    removal: Optional[datetime.date] = None


# получение данных аббонента
class Addendum(BaseModel):
    name: str
    numbers: str



# запись аббонента в справочник
class Record():
    id_user: Optional[str] = None
    name: Optional[str] = None
    numbers: Optional[str] = None



# вывод списка аббонента
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




# таблица токенов
class tokens(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    tokens: str
    date = date.today()

class App_token(SQLModel):
    tokens: str
