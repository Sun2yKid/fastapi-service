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

DATABASE_URI = os.getenv('DATABASE_URI') or 'mysql://root:zhonghui@localhost/movie_db'

engine = create_engine(DATABASE_URI)
metadata = MetaData()

casts = Table(
    'casts',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('nationality', String(20)),
)

database = Database(DATABASE_URI)
