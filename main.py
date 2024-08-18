from fastapi import FastAPI
from database import engineconn
from redis_config import redis_config

from src.user.router import router as user_router

app = FastAPI()
engine = engineconn()
session = engine.sessionmaker()
rd = redis_config()

app.include_router(user_router)
