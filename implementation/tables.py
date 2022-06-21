import sqlalchemy as sa

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

# таблица данных для записной книги
class Quide(Base):
    __tablename__ = 'phoneNumbers'
    id = sa.Column(sa.Integer, primary_key=True)
    id_user = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=True)
    name = sa.Column(sa.VARCHAR(100), nullable=True)
    numbers = sa.Column(sa.VARCHAR(20), nullable=True)
    date = sa.Column(sa.Date, nullable=True)
    update = sa.Column(sa.Date, nullable=True)


# таблица банных о пользователях справочника
class User(Base):
    __tablename__ = 'users'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.VARCHAR(100), nullable=True)
    password = sa.Column(sa.VARCHAR(100), nullable=True)
    date = sa.Column(sa.Date, nullable=True)
