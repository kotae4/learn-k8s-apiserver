from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select
from sqlalchemy.engine import URL

DATABASE_URL = URL.create(drivername="mysql+pymysql",
                          username="root",
                          password="toor",
                          host="db.testing.private",
                          port=3306,
                          database="appdb",
                          query={"charset": "utf8mb4"})

CONNECT_ARGS = {}

engine = create_engine(DATABASE_URL, echo=True, connect_args=CONNECT_ARGS)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_db() -> Session:
    with Session(engine) as session:
        yield session