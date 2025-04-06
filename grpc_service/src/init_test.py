import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine

# Загрузка переменных окружения
load_dotenv(dotenv_path="src/config/.env")

async def test_connection():
    db_url = f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    engine = create_async_engine(db_url, echo=True)

    try:
        async with engine.connect() as conn:
            result = await conn.execute("SELECT 1;")
            print("✅ Соединение установлено:", result.scalar())
    except Exception as e:
        print("❌ Ошибка подключения:", e)

if __name__ == "__main__":
    asyncio.run(test_connection())
