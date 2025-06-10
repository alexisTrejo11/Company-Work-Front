from fastapi import FastAPI
from model_initialization import *
from app.movies.infrastructure.api import movie_controllers
from app.movies.infrastructure.api import movie_showtime_controller
from app.cinema.infrastructure.api import cinema_controllers
from app.theater.infrastructure.api.controllers import theater_controllers, theather_seat_controllers
from app.showtime.infrastructure.api import showtime_controller
from config import exception_handlers

app = FastAPI(
        title="Cinema Backend: Billboard Service API",
        version="1.0.0",
        exception_handlers=exception_handlers
    )

@app.get("/")
def read_home():
    return { "home": "Welcome To Billboard Service" } 

app.include_router(movie_controllers.router)
app.include_router(movie_showtime_controller.router)

app.include_router(cinema_controllers.router)

app.include_router(theater_controllers.router)
app.include_router(theather_seat_controllers.router)

app.include_router(showtime_controller.router)