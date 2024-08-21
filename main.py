from fastapi import FastAPI, HTTPException
from core.database import engineconn
from core.redis_config import redis_config

from core.exceptions import generic_exception_handler, BaseCustomException, base_custom_exception_handler

from src.user.router import router as user_router
from src.content.router import router as content_router

app = FastAPI()
engine = engineconn()
session = engine.sessionmaker()
rd = redis_config()

# Exception handler
app.add_exception_handler(HTTPException, generic_exception_handler)
app.add_exception_handler(BaseCustomException, base_custom_exception_handler)

# Router
app.include_router(user_router)
app.include_router(content_router)
