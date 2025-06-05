from fastapi import FastAPI
from app.models import *
from app.movies.infrastructure.api.controllers import movie_controllers
from app.cinema.infrastructure.api.controllers import cinema_controllers
from app.theater.infrastructure.api.controllers import theater_controllers, theather_seat_controllers
from app.showtime.infrastructure.api.controllers import showtime_command_controller, showtime_query_controller
from app.config import exception_handlers

app = FastAPI(
        title="Cinema Backend: Billboard Service API",
        version="1.0.0",
        exception_handlers=exception_handlers
    )

@app.get("/")
def read_home():
    return { "home": "Welcome To Billboard Service" } 

app.include_router(movie_controllers.router)
app.include_router(cinema_controllers.router)

app.include_router(theater_controllers.router)
app.include_router(theather_seat_controllers.router)

app.include_router(showtime_command_controller.router)
app.include_router(showtime_query_controller.router)