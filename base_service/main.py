from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from .src.routing.routing import main_router
from .src.config.config import load_env


import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



app = FastAPI()
load_env()

app.include_router(main_router)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"An error occurred: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"},
    )
