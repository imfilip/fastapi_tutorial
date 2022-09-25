from lib2to3.pytree import Base
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


# CRUD aplication - Create Read Update Delete

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

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

@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * FROM POSTS""")
    posts = cursor.fetchall()
    return {"data": posts}

# @app.post("/createposts")
@app.post("/posts", status_code=status.HTTP_201_CREATED)
# async def create_posts(payload: dict = Body(...)):
async def create_posts(post: Post):
    # # print(post)
    # # print(post.dict())
    # post_dict = post.dict()
    # post_dict["id"] = randrange(0, 10000000)
    # my_posts.append(post_dict)
    # # return {"post": f"title: {payload['title']} || content: {payload['content']}"}
    # return {"data": post_dict}

    # cursor.execute(f"INSERT INTO posts (title, content, published) VALUES ({post.title}, {post.content}, {post.published}) ") # Tak nie rób! Wrażliwe na ataki!
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    
    conn.commit()
    
    return {"data": new_post}

@app.get("/posts/latest") # Tutaj jest ważna kolejność, żeby fastapi nie potraktował 'latest' jako "id"
async def get_latest_post():
    cursor.execute(""" SELECT * FROM posts ORDER BY created_at DESC """)
    post = cursor.fetchone()
    return {"post_detail": post}

@app.get("/posts/{id}")
async def get_post(id: int): #, response: Response):
    # post = find_post(id)
    # if not post:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
    #         detail = f"post with id: {id} was not found")
    #     # response.status_code = status.HTTP_404_NOT_FOUND
    #     # return {"meassage": f"post with id: {id} was not found"}
    # return {"post_detail": post}
    
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),)) # str jest traktowany jak lista, bez tego przecinka przy id > 9 wyrzuca błąd. 
    # Chodzi o to, że dla np. 10 próbuje znaleźć dwie zmienne i podać liczby 1 oraz 0. 
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail = f"post with id: {id} was not found")
    
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    # index = find_post_index(id)
    # if index == None:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
    #         detail = f"post with id: {id} does not exist")
    # my_posts.pop(index)

    cursor.execute(""" DELETE FROM posts WHERE ID = %s RETURNING * """, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail = f"post with id: {id} does not exist")

    # return {"message": "The post has been deleted"} - jak działanie kończy się statusem 204, to klient nie oczekuję od nas żadnych dodatkowych danych
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    # index = find_post_index(id)
    # if index == None:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
    #         detail = f"post with id: {id} does not exist")
    # post_dict = post.dict()
    # post_dict["id"] = id
    # my_posts[index] = post_dict

    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, 
        (post.title, post.content, post.published, str(id),))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail = f"post with id: {id} does not exist")

    return {"data": updated_post}