from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from core.config import settings
from core.base import Base
from src.user.models import User

DB_URL = f'mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'

class engineconn:
    def __init__(self):
        self.engine = create_engine(DB_URL, echo=True, pool_recycle=500)
        try:
            with self.engine.begin() as connection:
                print(f"DB connected. >>> {self.engine.url}")
                self.create_tables()
        except Exception as e:
            print(f"DB connection failed.\n{e}")

    def sessionmaker(self):
        Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        session = Session()
        return session

    def connection(self):
        conn = self.engine.connect()
        return conn

    def create_tables(self):
        print("Creating tables...")
        Base.metadata.create_all(bind=self.engine)

# DB Session
def get_db():
    db = engineconn().sessionmaker()
    try:
        yield db
    finally:
        db.close()
