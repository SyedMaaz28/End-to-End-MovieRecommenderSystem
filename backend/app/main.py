from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import health, recommend
from app.ml.loader import load_pickles

from app.api.routes import (
    health,
    recommend,
    tmdb,
    movie,
    home,
)



app = FastAPI(title="Movie Recommender API", version="3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    load_pickles()

app.include_router(health.router)
app.include_router(recommend.router)
app.include_router(tmdb.router)
app.include_router(movie.router)
app.include_router(home.router)



app.include_router(health.router)
app.include_router(recommend.router)
