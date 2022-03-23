from fastapi import FastAPI

from database import Base, engine
from posts.router import router as posts_router
from news_api.parser import router as api_router
from users.router import router as users_router

Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(posts_router)
app.include_router(api_router)
app.include_router(users_router)