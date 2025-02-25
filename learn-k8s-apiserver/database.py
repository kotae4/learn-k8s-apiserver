from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select
from sqlalchemy.engine import URL, Engine
from sqlalchemy import text
from typing_extensions import Annotated
from fastapi import Depends
from . import config

_engine = None
def get_engine() -> Engine:
    global _engine
    settings = config.get_settings()
    if _engine is None:
        db_url = URL.create(drivername=settings.db_driver,
                          username=settings.db_username,
                          password=settings.db_password,
                          host=settings.db_host,
                          port=settings.db_port,
                          query={"charset": "utf8mb4"})
        connection_args = {'connect_timeout': 10}
        tmpEngine = create_engine(db_url, connect_args=connection_args)
        with tmpEngine.connect() as conn:
            create_db_query = f"CREATE DATABASE IF NOT EXISTS `{settings.db_database}`;"
            conn.execute(text(create_db_query))
            conn.commit()
        db_url = db_url.set(database=settings.db_database)
        _engine = create_engine(db_url, pool_pre_ping=True, pool_timeout=30, echo_pool=True, echo=settings.db_echo, connect_args=connection_args)

    return _engine

def create_db_and_tables():
    SQLModel.metadata.create_all(get_engine())

def get_db() -> Session:
    with Session(get_engine()) as session:
        yield session