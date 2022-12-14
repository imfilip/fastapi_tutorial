
from fastapi import Body, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import posts, users, auth, votes
from .config import settings


# Jak już korzystam z alembic, to ten fragment nie jest potrzebny. On odpowiada za stworzenie modeli na bazie, jeżeli ich wcześniej nie było.
# models.Base.metadata.create_all(bind=engine) # Z jakiegoś powodu jednak zostawiłem ten kod. Ale musze go wyłączyć, bo jak puszczam testy na github, to mi wywala, bo chce, żebym miał produkcyjną bazę danych fastapi.

# CRUD aplication - Create Read Update Delete

app = FastAPI()

# Sprawdzałem na Google Chrome i faktycznie zaczyna działać z podanych stron przez konsolę przeglądarki.
# Na Brave mam jakiś inny problem.
# origins = ["https://www.google.com", "https://www.youtube.com"]
origins = ["*"]
# To się na pewno przyda jak będziemy chcieli łączyć frontend i api - będę musiał podać w origins adres frontendu, żeby to działało.

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/", tags = ["index"])# for the purpose of testing:  , status_code=status.HTTP_201_CREATED)
async def root():
    return {"message": "chyba nie?",
        "task": "Change your URL adding sufix /docs. Try the app out creating firstly a new user and next after the authentication (green button with padlock and 'Authorize' word) creating posts. Have fun dude! :)",
        "remark": "Why haven't you changed anything?"}