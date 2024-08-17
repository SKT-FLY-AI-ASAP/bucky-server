from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from config import settings
from base import Base
from src.user.models import User

DB_URL = f'mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'

class engineconn:
    def __init__(self):
        self.engine = create_engine(DB_URL, echo=True, pool_recycle=500)

    def sessionmaker(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def connection(self):
        conn = self.engine.connect()
        return conn

    def create_tables(self):
        print("Creating tables...")
        Base.metadata.create_all(bind=self.engine)
