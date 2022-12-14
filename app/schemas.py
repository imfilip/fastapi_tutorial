from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    password: str
class UserCreate(UserBase):
    pass

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class UserLogin(UserBase):
    pass

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True

class PostResponseVotes(BaseModel):
    Posts: PostResponse # Musze wielka litera Posts, poniewaz SQLAlchemy model tez jest wielka litera Posts.
    votes: int


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # tutaj chce zeby bylo albo zero albo 1, ale to conint zapewnia mi, ze sa to integer less equal 1.