from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from app.api.movies import movies

app = FastAPI()

app.include_router(movies)
