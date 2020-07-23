import json

from typing import List, Optional
from pydantic import BaseModel
import sqlalchemy.types as types


class MovieIn(BaseModel):
    name: str
    plot: str
    genres: List[str]
    casts_id: List[int]


class MovieOut(MovieIn):
    id: int


class MovieUpdate(MovieIn):
    name: Optional[str] = None
    plot: Optional[str] = None
    genres: Optional[List[str]] = None
    casts_id: Optional[List[int]] = None


class Movie(BaseModel):
    name: str
    plot: str
    genres: List[str]
    casts: List[str]


class TextJson(types.TypeDecorator):
    """
    自带json dump load的数据类型
    """
    impl = types.TEXT

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return json.loads(value)
