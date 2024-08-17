from fastapi import FastAPI
from database import engineconn

app = FastAPI()
engine = engineconn()
session = engine.sessionmaker()

def check_connection():
    try:
        with engine.engine.begin() as connection:
            print(f"DB connected. >>> {engine.engine.url}")
            engine.create_tables()
    except Exception as e:
        print(f"DB connection failed.\n{e}")

check_connection()
