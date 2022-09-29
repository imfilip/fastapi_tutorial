
from statistics import mode
from turtle import title
from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session

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


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts", response_model = List[schemas.PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM POSTS""")
    # posts = cursor.fetchall()
    posts = db.query(models.Posts).all()
    return posts

# @app.post("/createposts")
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model = schemas.PostResponse)
# async def create_posts(payload: dict = Body(...)):
async def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # # print(post)
    # # print(post.dict())
    # post_dict = post.dict()
    # post_dict["id"] = randrange(0, 10000000)
    # my_posts.append(post_dict)
    # # return {"post": f"title: {payload['title']} || content: {payload['content']}"}
    # return {"data": post_dict}

    # cursor.execute(f"INSERT INTO posts (title, content, published) VALUES ({post.title}, {post.content}, {post.published}) ") # Tak nie rób! Wrażliwe na ataki!
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    
    # conn.commit()
    new_post = models.Posts(**post.dict()) # moja propozycja
    # new_post = models.Posts(title = post.title, content = post.content, published = post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/latest", response_model = schemas.PostResponse) # Tutaj jest ważna kolejność, żeby fastapi nie potraktował 'latest' jako "id"
async def get_latest_post(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts ORDER BY created_at DESC """)
    # post = cursor.fetchone()
    post = db.query(models.Posts).order_by(models.Posts.created_at.desc()).first()
    return post

@app.get("/posts/{id}", response_model = schemas.PostResponse)
async def get_post(id: int, db: Session = Depends(get_db)): #, response: Response):
    # post = find_post(id)
    # if not post:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
    #         detail = f"post with id: {id} was not found")
    #     # response.status_code = status.HTTP_404_NOT_FOUND
    #     # return {"meassage": f"post with id: {id} was not found"}
    # return {"post_detail": post}
    
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),)) # str jest traktowany jak lista, bez tego przecinka przy id > 9 wyrzuca błąd. 
    # Chodzi o to, że dla np. 10 próbuje znaleźć dwie zmienne i podać liczby 1 oraz 0. 
    # post = cursor.fetchone()

    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail = f"post with id: {id} was not found")
    
    return post


@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    # index = find_post_index(id)
    # if index == None:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
    #         detail = f"post with id: {id} does not exist")
    # my_posts.pop(index)

    post = db.query(models.Posts).filter(models.Posts.id == id)

    # cursor.execute(""" DELETE FROM posts WHERE ID = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    if post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail = f"post with id: {id} does not exist")

    post.delete(synchronize_session=False)
    db.commit()

    # return {"message": "The post has been deleted"} - jak działanie kończy się statusem 204, to klient nie oczekuję od nas żadnych dodatkowych danych
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", response_model = schemas.PostResponse)
async def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # index = find_post_index(id)
    # if index == None:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
    #         detail = f"post with id: {id} does not exist")
    # post_dict = post.dict()
    # post_dict["id"] = id
    # my_posts[index] = post_dict

    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, 
    #     (post.title, post.content, post.published, str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    post = post_query.first()


    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail = f"post with id: {id} does not exist")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()


@app.get("/sqlalchemy/", response_model = List[schemas.PostResponse])
async def get_db(db: Session = Depends(get_db)):
    posts = db.query(models.Posts).all()
    return posts


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model = schemas.UserCreate)
# async def create_posts(payload: dict = Body(...)):
async def create_posts(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # # print(post)
    # # print(post.dict())
    # post_dict = post.dict()
    # post_dict["id"] = randrange(0, 10000000)
    # my_posts.append(post_dict)
    # # return {"post": f"title: {payload['title']} || content: {payload['content']}"}
    # return {"data": post_dict}

    # cursor.execute(f"INSERT INTO posts (title, content, published) VALUES ({post.title}, {post.content}, {post.published}) ") # Tak nie rób! Wrażliwe na ataki!
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    
    # conn.commit()
    new_user = models.Posts(**user.dict()) # moja propozycja
    # new_post = models.Posts(title = post.title, content = post.content, published = post.published)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
