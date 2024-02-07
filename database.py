from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select
from sqlalchemy.engine import URL, Engine
from typing_extensions import Annotated
from fastapi import Depends
from . import config

_engine = None
def get_engine(settings: Annotated[config.Settings, Depends(config.get_settings)]) -> Engine:
    if _engine is None:
        db_url = URL.create(drivername=settings.db_driver,
                          username=settings.db_username,
                          password=settings.db_password,
                          host=settings.db_host,
                          port=settings.db_port,
                          database=settings.db_database,
                          query={"charset": "utf8mb4"})
        connection_args = {}
        _engine = create_engine(db_url, echo=settings.db_echo, connect_args=connection_args)
    return _engine

def create_db_and_tables():
    SQLModel.metadata.create_all(get_engine())

def get_db() -> Session:
    with Session(get_engine()) as session:
        yield session