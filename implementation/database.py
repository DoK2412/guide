from implementation.settings import setting
from sqlmodel import Session, create_engine

# подключение к базе
engin = create_engine(
    setting.database_url
)


async def get_session():
    with Session(engin) as session:
        yield session