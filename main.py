import uvicorn
from fastapi import FastAPI
from config import settings
from database import engineconn

app = FastAPI()

def check_connection():
    engine = engineconn().engine
    try:
        with engine.begin() as connection:
            print(f"DB connected. >>> {engine.url}")
    except Exception as e:
        print(f"DB connection failed.\n{e}")

check_connection()
