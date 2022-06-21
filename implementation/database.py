from sqlalchemy import create_engine
from  sqlalchemy.orm import sessionmaker
from implementation.settings import setting

# подключение к базе
engin = create_engine(
    setting.database_url
)

# создание сессии для работы
Session = sessionmaker(
    engin,
    autoflush=False,
    autocommit=False
)

# функция автоматизации сессий
async def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()
