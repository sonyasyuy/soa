from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from collections import defaultdict
from base_service.src.usecase.usecase import add_new_user, check_auth_user, update_user
from base_service.src.repo.repository import Repository
from base_service.src.models.models import NewUser, AuthUser, UpdateUser
from datetime import datetime, timedelta

import json

main_router = APIRouter()


@main_router.post('/register', status_code=201)
async def register_new_user(request: Request, _: NewUser):
    input_data = await request.body()
    if not input_data:
        return JSONResponse(content={"message": "invalid input data"}, status_code=400)
    data_input = defaultdict(str, json.loads(input_data))

    try:
        new_id = await add_new_user(data_input)
    except ValueError as e:
        raise HTTPException(400, {"message": str(e)})

    if new_id <= 0:
        raise HTTPException(500, {"message": "error in create user"})

    return JSONResponse(content={"message": "You've been successfully registered"}, status_code=200)


@main_router.post("/auth", status_code=201)
async def auth_user(request: Request, _: AuthUser):
    input_data = await request.body()
    if not input_data:
        return JSONResponse(content={"message": "invalid input data"}, status_code=400)
    data_input = defaultdict(str, json.loads(input_data))
    if "nickname" not in data_input or "password" not in data_input:
        raise HTTPException(400, {"message": "not enough data for check user"})
    try:
        res = await check_auth_user(data_input['nickname'], data_input['password'])
    except ValueError as e:
        raise HTTPException(400, {"message": str(e)})

    if not res:
        raise HTTPException(400, {"message": "wrong password, try again!"})

    return JSONResponse(content={"message": "You've been successfully authorized"}, status_code=200)



@main_router.get('/get', status_code=200)
async def get_users():
    values = await Repository().get_users()
    return values


@main_router.put("/update", status_code=200)
async def update_data_user(request: Request, _: UpdateUser):
    input_data = await request.body()
    if not input_data:
        return JSONResponse(content={"message": "no data for update"}, status_code=400)
    data_input = defaultdict(str, json.loads(input_data))
    try:
        await update_user(data_input)
    except ValueError as e:
        return JSONResponse(content={"message": str(e)})

    return JSONResponse(content={"message": "data succesfully updated"}, status_code=200)


