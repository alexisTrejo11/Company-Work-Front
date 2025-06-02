from fastapi import FastAPI
from .movies.infrastructure.api.controllers import movie_controllers
from .cinema.infrastructure.api.controllers import cinema_controllers
app = FastAPI()

@app.get("/")
def read_home():
    return { "home": "Welcome To Billboard Service" } 

app.include_router(movie_controllers.router)
app.include_router(cinema_controllers.router)
