from fastapi import FastAPI
from app.infrastructure.persistence.v1.api.endpoints import movie_controllers


app = FastAPI()

@app.get("/")
def read_home():
    return { "home": "Welcome To Billboard Service" } 

app.include_router(movie_controllers.router)
