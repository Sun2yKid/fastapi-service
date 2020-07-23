import json
import os

from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine, ARRAY, types

from databases import Database


class TextJson(types.TypeDecorator):
    impl = types.TEXT

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return json.loads(value)


# DATABASE_URI = 'mysql://root:zhonghui@localhost/movie_db'
DATABASE_URI = os.getenv('DATABASE_URI')

engine = create_engine(DATABASE_URI)
metadata = MetaData()

movies = Table(
    'movies',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('plot', String(250)),
    Column('genres', TextJson),
    Column('casts', TextJson)
)

database = Database(DATABASE_URI)
