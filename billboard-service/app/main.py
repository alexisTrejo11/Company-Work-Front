from typing import Union

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_home():
    return { "home": "Welocme To Billboard Service" } 