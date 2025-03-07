import asyncpg # библиотека для асинхронного доступа к PostgreSQL
import os


async def connection_start():
    connection = await asyncpg.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )

    return connection