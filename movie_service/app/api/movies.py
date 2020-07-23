from typing import List
from fastapi import Header, APIRouter, HTTPException

from app.api.models import Movie, MovieIn, MovieOut
from app.api import db_manager
from app.api.service import is_cast_present

# fake_movie_db = [
#     {
#         'name': 'Star Wars: Episode IX - The Rise of Skywalker',
#         'plot': 'The surviving members of the resistance face the First Order once again.',
#         'genres': ['Action', 'Adventure', 'Fantasy'],
#         'casts': ['Daisy Ridley', 'Adam Driver']
#     }
# ]

movies = APIRouter()


# @movies.get('/', response_model=List[Movie])
# async def index():
#     return fake_movie_db


@movies.get('/', status_code=201)
async def index():
    return await db_manager.get_all_movies()


@movies.get('/{id}/', response_model=MovieOut)
async def get_movie(id: int):
    movie = await db_manager.get_movie(id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


# @movies.post('/', status_code=201)
# async def add_movie(payload: Movie):
#     movie = payload.dict()
#     fake_movie_db.append(movie)
#     return {'id': len(fake_movie_db) - 1}


@movies.post('/', status_code=201)
async def add_movie(payload: MovieIn):
    movie_id = await db_manager.add_movie(payload)
    response = {
        'id': movie_id,
        **payload.dict()
    }
    return response


@movies.post('/', response_model=List[MovieOut], status_code=201)
async def create_movies(payload: MovieIn):
    for cast_id in payload.casts_id:
        if not is_cast_present(cast_id):
            raise HTTPException(status_code=404, detail=f"Cast with id:{cast_id} not found")

    movie_id = await db_manager.add_movie(payload)
    response = {
        'id': movie_id,
        **payload.dict()
    }
    return response


# @movies.put('/{id}')
# async def update_movie(id: int, payload: Movie):
#     movie = payload.dict()
#     movies_length = len(fake_movie_db)
#     if 0 <= id <= movies_length:
#         raise HTTPException(status_code=404, detail="Movie with given id not found")
#     fake_movie_db[id] = movie
#     return None


@movies.put('/{id}', response_model=MovieOut)
async def update_movie(id: int, payload: MovieIn):
    movie = await db_manager.get_movie(id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    update_data = payload.dict(exclude_unset=True)

    if 'casts_id' in update_data:
        for cast_id in payload.casts_id:
            if not is_cast_present(cast_id):
                raise HTTPException(status_code=404, detail=f"Cast with given id:{cast_id} not found")

    movie_in_db = MovieIn(**movie)

    updated_movie = movie_in_db.copy(update=update_data)
    return await db_manager.update_movie(id, updated_movie)


# @movies.delete('/{id}')
# async def delete_movie(id: int):
#     movies_length = len(fake_movie_db)
#     if 0 <= id <= movies_length:
#         raise HTTPException(status_code=404, detail="Movie with given id not found")
#     del fake_movie_db[id]
#     return None


@movies.delete('/{id}')
async def delete_movie(id: int):
    movie = await db_manager.get_movie(id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return await db_manager.delete_movie(id)
