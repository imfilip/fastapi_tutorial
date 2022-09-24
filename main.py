from lib2to3.pytree import Base
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

# CRUD aplication - Create Read Update Delete

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

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
    return {"data": my_posts}

# @app.post("/createposts")
@app.post("/posts", status_code=status.HTTP_201_CREATED)
# async def create_posts(payload: dict = Body(...)):
async def create_posts(post: Post):
    # print(post)
    # print(post.dict())
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 10000000)
    my_posts.append(post_dict)
#    return {"post": f"title: {payload['title']} || content: {payload['content']}"}
    return {"data": post_dict}

@app.get("/posts/latest") # Tutaj jest ważna kolejność, żeby fastapi nie potraktował 'latest' jako "id"
async def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"post_detail": post}

@app.get("/posts/{id}")
async def get_post(id: int): #, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail = f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"meassage": f"post with id: {id} was not found"}
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail = f"post with id: {id} does not exist")
    my_posts.pop(index)
    # return {"message": "The post has been deleted"} - jak działanie kończy się statusem 204, to klient nie oczekuję od nas żadnych dodatkowych danych
    return Response(status_code=status.HTTP_204_NO_CONTENT)
