from fastapi import FastAPI
from .src.routing.routing import main_router
from .src.config.config import *


app = FastAPI()
load_env()

app.include_router(main_router)