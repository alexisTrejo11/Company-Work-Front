from fastapi import FastAPI
from app.models import *
from app.movies.infrastructure.api.controllers import movie_controllers
from app.cinema.infrastructure.api.controllers import cinema_controllers
from app.theater.infrastructure.api.controllers import theater_controllers
app = FastAPI()

@app.get("/")
def read_home():
    return { "home": "Welcome To Billboard Service" } 

app.include_router(movie_controllers.router)
app.include_router(cinema_controllers.router)
app.include_router(theater_controllers.router)
