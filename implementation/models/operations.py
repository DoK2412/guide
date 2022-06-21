from pydantic import BaseModel


class Operation(BaseModel):
    id: int
    name: str
    numbers: str

    class Coufig:
        orm_mode= True

# добавление пользователя
class Addendum(BaseModel):
    name: str
    tel: str

# обновление контакта
class Update(BaseModel):
    id: int
    name: str = None
    tel: str = None

# удаление коетакта
class Delete(BaseModel):
    id: int

# регистрация пользователя
class Сreatings(BaseModel):
    name: str
    password: str

# вход пользователя
class Authorization(BaseModel):
    name: str
    password: str
