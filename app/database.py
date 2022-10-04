from requests import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db(): #-> Generator: # from typing
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pierwszy sposob łaczenia się z bazą danych. Teraz używam SQLAlchemy, ktory ma wbudowany driver (poza ORM)
# while True:
#     try: 
#         conn = psycopg2.connect(host = 'localhost', database = 'fastapi', 
#             user = 'postgres', password = 'admin', cursor_factory = RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successfull!")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print(f"Error: {error}")
#         time.sleep(2)


# Zanim zaczelismy uzywac PostgreSQL, to dane przechowywalem tutaj:
# my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
#     {"title": "favorite foods", "content": "I like pizza!", "id": 2}]

# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p

# def find_post_index(id):
#     for i, p in enumerate(my_posts): # zobacz dokumentację: https://realpython.com/python-enumerate/
#         if p["id"] == id:
#             return i
