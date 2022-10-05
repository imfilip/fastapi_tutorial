
from fastapi import Body, FastAPI
from . import models
from .database import engine
from .routers import posts, users, auth, votes
from .config import settings

models.Base.metadata.create_all(bind=engine)

# CRUD aplication - Create Read Update Delete

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/", tags = ["index"])
async def root():
    return {"message": "Hello World"}