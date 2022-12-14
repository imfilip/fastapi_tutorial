from optparse import Option
from .. import models, schemas, oauth2
from fastapi import Body, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

router = APIRouter(
    prefix = "/posts",
    tags = ["posts"]
)

# @router.get("/", response_model = List[schemas.PostResponse])
@router.get("/", response_model = List[schemas.PostResponseVotes])
async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
    limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM POSTS""")
    # posts = cursor.fetchall()
    # posts = db.query(models.Posts).filter(models.Posts.owner_id == current_user.id).all()
    
    # posts = db.query(models.Posts).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Posts, func.count(models.Votes.post_id).label("votes")).join(models.Votes, 
        models.Posts.id == models.Votes.post_id, isouter = True).group_by(models.Posts.id).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()
    return posts# results[0][0]

# @app.post("/createposts")
@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.PostResponse)
# async def create_posts(payload: dict = Body(...)):
async def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)): # user_id, bo tak zdecydowałem w ayth.py - ze do tworzenia jwt tokenu bede uzywal tylko id uzytkownika
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
    # print(user_id)
    # print(current_user.email)
    # print(current_user.id)
    
    # Doklejanie owner_id - jest lepszy sposób
    # post = post.dict()
    # post["owner_id"] = current_user.id

    new_post = models.Posts(owner_id = current_user.id, **post.dict()) # moja propozycja
    # new_post = models.Posts(title = post.title, content = post.content, published = post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/latest", response_model = schemas.PostResponse) # Tutaj jest ważna kolejność, żeby fastapi nie potraktował 'latest' jako "id"
async def get_latest_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts ORDER BY created_at DESC """)
    # post = cursor.fetchone()
    post = db.query(models.Posts).order_by(models.Posts.created_at.desc()).first()
    return post

@router.get("/{id}", response_model = schemas.PostResponseVotes)
async def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): #, response: Response):
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
    
    post = db.query(models.Posts, func.count(models.Votes.post_id).label("votes")).join(models.Votes, 
        models.Posts.id == models.Votes.post_id, isouter = True).group_by(models.Posts.id).filter(models.Posts.id == id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail = f"post with id: {id} was not found")

    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #         detail = f"Not authorized to perform requested action")
    
    return post


@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # index = find_post_index(id)
    # if index == None:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
    #         detail = f"post with id: {id} does not exist")
    # my_posts.pop(index)

    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    post = post_query.first()

    # cursor.execute(""" DELETE FROM posts WHERE ID = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail = f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
            detail = f"Not authorized to perform requested action")


    post_query.delete(synchronize_session=False)
    db.commit()

    # return {"message": "The post has been deleted"} - jak działanie kończy się statusem 204, to klient nie oczekuję od nas żadnych dodatkowych danych
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model = schemas.PostResponse)
async def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
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

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
            detail = f"Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()

# Jak zostawiam kod poniżej, to api przestaje dzialac - jako db przypisuje mi liste.
# Znalazlem rozwiazanie - funkcja, ktora uzywalem pod tym adresem nazywala sie tak samo jak funkcja wywolujaco polaczenie z db - get_db 
# @router.get("/sqlalchemy", response_model = List[schemas.PostResponse], tags = ["posts"])
# async def get_alldata(db: Session = Depends(get_db)):
#     print(db)
#     posts = db.query(models.Posts).all()
#     return posts
