import datetime

from base_service.src.repo.init_db import connection_start
from collections import defaultdict


class Repository:

    async def get_users(self) -> list:
        conn = await connection_start()
        values = await conn.fetch('''SELECT * FROM users''')
        await conn.close()
        return values

    async def get_user_nick(self, nick: str) -> int:
        conn = await connection_start()
        value = await conn.fetch(f"SELECT id FROM users WHERE nickname='{nick}'")
        await conn.close()
        if len(value) == 0:
            return -1
        return value[0]['id']


    async def check_user(self, nick: str) -> bool:
        conn = await connection_start()
        values = await conn.fetch(f"SELECT * FROM users WHERE nickname='{nick}'")
        await conn.close()
        return bool(values)

    async def ret_auth_data(self, login: str) -> str: # авторизация пользователя
        conn = await connection_start()
        hash = await conn.fetch(f"SELECT password FROM users WHERE nickname='{login}'")
        await conn.close()
        return hash


    async def update_last_login(self, login: str) -> None:
        conn = await connection_start()
        await conn.execute("UPDATE users SET updated_at = NOW() WHERE nickname = $1", login)
        await conn.close()


    async def add_user(self, data: defaultdict) -> int:
        conn = await connection_start()
        new_id = await conn.fetch(f"""INSERT INTO users (
                                      nickname, "password", email, phone_number, "name", surname, birth_date, created_at, updated_at
                                      ) 
                                      VALUES (
                                      '{data['nickname']}', 
                                      '{data['password']}', 
                                      '{data['email']}', 
                                      '{data['phone_number']}', 
                                      '{data['name']}',
                                      '{data['surname']}', 
                                      CASE WHEN ('{data['birth_date']}' <> '') IS FALSE THEN CAST(NULL as DATE)
                                           ELSE '{data['birth_date'] or '2002-10-05'}'
                                      END,
                                      NOW(),
                                      NOW()
                                      ) RETURNING id""")
        await conn.close()
        return new_id[0]['id']

    async def update_user(self,data: dict) -> None:
        conn = await connection_start()
        for i, v in data.items():
            await conn.fetch(f"""UPDATE users SET {i}='{v}'""")
        await conn.close()

    async def get_user_by_nickname(self, nickname: str):
        conn = await connection_start()
        result = await conn.fetch("SELECT * FROM users WHERE nickname = $1", nickname)
        await conn.close()
        if result:
            return result[0]
        return None

    async def update_user_by_nickname(self, nickname: str, fields: dict) -> None:
        conn = await connection_start()
        set_expr = []
        values = []
        idx = 1
        for field, value in fields.items():
            set_expr.append(f"{field} = ${idx}")
            values.append(value)
            idx += 1
        # Всегда обновляем updated_at
        set_expr.append("updated_at = NOW()")
        query = f"UPDATE users SET {', '.join(set_expr)} WHERE nickname = ${idx}"
        values.append(nickname)

        await conn.execute(query, *values)
        await conn.close()