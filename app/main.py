
from msilib import schema
from statistics import mode
from turtle import title
from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import posts, users, auth


models.Base.metadata.create_all(bind=engine)

# CRUD aplication - Create Read Update Delete

app = FastAPI()

while True:
    try: 
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi', 
            user = 'postgres', password = 'admin', cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print(f"Error: {error}")
        time.sleep(2)

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favorite foods", "content": "I like pizza!", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_post_index(id):
    for i, p in enumerate(my_posts): # zobacz dokumentację: https://realpython.com/python-enumerate/
        if p["id"] == id:
            return i


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/", tags = ["index"])
async def root():
    return {"message": "Hello World"}

