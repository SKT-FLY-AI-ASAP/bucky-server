from fastapi import FastAPI, HTTPException
from core.database import engineconn
from core.redis_config import redis_config

from core.exceptions import value_error_handler, generic_exception_handler

from src.user.router import router as user_router

app = FastAPI()
engine = engineconn()
session = engine.sessionmaker()
rd = redis_config()

# Exception handler
app.add_exception_handler(ValueError, value_error_handler)
app.add_exception_handler(HTTPException, generic_exception_handler)

# Router
app.include_router(user_router)
