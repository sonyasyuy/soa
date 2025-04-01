import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
# Загрузка переменных окружения из .env
load_dotenv(dotenv_path='src/config/.env')

# Чтение параметров подключения
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "posts")
DB_USER = os.getenv("DB_USER", "posts")
DB_PASS = os.getenv("DB_PASS", "posts")

# Асинхронный URL для SQLAlchemy
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"

# Создание асинхронного движка и сессии
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

# Базовый класс для моделей
Base = declarative_base()
