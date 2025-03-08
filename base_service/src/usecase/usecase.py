from base_service.src.repo.repository import *
from collections import defaultdict
from datetime import timedelta, time

import datetime, time


async def preprocess_date(date: str) -> bool:
    try:
        x = time.strptime(date, '%Y-%m-%d')
    except ValueError:
        return False
    return True


async def add_new_user(data: dict) -> int:
    unfill = []
    for i in ["nickname", "password"]:
        if i not in data:
            unfill.append(i)
    if unfill:
        raise ValueError(f"not enough fields in data for register, you need to fill: {', '.join(unfill)}")

    if len(data['nickname']) <= 4:
        raise ValueError("very low length of your nickname, please try again with length > 4")

    exists = await check_user(data['nickname'])

    if exists:
        raise ValueError("this user already exists!")

    if 'birth_date' in data and not await preprocess_date(data['birth_date']):
        raise ValueError("wrong birth date!")

    if len(data['password']) <= 5:
        raise ValueError("very low length of passsword, try minimum 6 symbols!")

    return await Repository().add_user(defaultdict(str, data))


async def check_auth_user(login: str, password: str) -> bool:
    if not await check_user(login):
        raise ValueError("this user doesn't exist")
    # Получаем хэшированный пароль из базы данных
    hash_p = await Repository().ret_auth_data(login)
    if hash_p[0]['password'] == password:
        # Обновляем updated_at в таблице users для данного пользователя
        await Repository().update_last_login(login)
        return True
    else:
        return False


async def check_user(nick: str):
    return await Repository().check_user(nick)


async def update_user(data: dict):
    # Обязательно должен быть nickname для идентификации пользователя
    nickname = data.get("nickname")
    if not nickname:
        raise ValueError("Nickname is required for update")

    # Удаляем nickname, чтобы не пытаться его обновить
    data.pop("nickname", None)

    repo = Repository()
    user = await repo.get_user_by_nickname(nickname)
    if not user:
        raise ValueError("User not found")

    if datetime.datetime.utcnow() - user["updated_at"] > timedelta(hours=1):
        raise ValueError("Session expired, please reauthenticate")

    # Разрешённые поля для обновления
    allowed_fields = ["email", "phone_number", "name", "surname", "birth_date"]
    fields_for_update = {}
    for field, value in data.items():
        if field in allowed_fields:
            fields_for_update[field] = value
        elif field in ["password"]:
            raise ValueError(f"Field '{field}' is not allowed for updating")

    # Если передана birth_date, преобразуем строку в объект date
    if "birth_date" in fields_for_update:
        try:
            fields_for_update["birth_date"] = datetime.datetime.strptime(
                fields_for_update["birth_date"], "%Y-%m-%d"
            ).date()
        except ValueError:
            raise ValueError("Wrong birth date format. Use YYYY-MM-DD")

    await repo.update_user_by_nickname(nickname, fields_for_update)
