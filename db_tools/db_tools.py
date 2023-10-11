import os

from dotenv import load_dotenv
# import psycopg2

from sqlalchemy import create_engine, Table, insert
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData

# Load the environment variables from the .env file
load_dotenv()


class Connect:
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    DB_PORT = int(os.getenv("DB_PORT"))

    def __init__(self):
        self.sqlalchemy_engine = self.sqlalchemy_engine()

    def sqlalchemy_engine(self):
        engine = create_engine(
            f'postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}')
        return engine

    def create_session(self):
        engine = self.sqlalchemy_engine
        session = sessionmaker(bind=engine)
        session = session()
        return session

    def alchemy_post_mult_data(self, dbschema: str, table_name: str, value_list: list):
        table = Table(table_name, MetaData(dbschema), autoload_with=self.sqlalchemy_engine)
        sess = self.create_session()
        query = insert(table).values(value_list)
        sess.execute(query)
        sess.commit()
        sess.close()
