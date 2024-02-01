from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker
from config.constants import (
    DRIVERNAME,
    DB_HOSTNAME,
    DB_NAME,
    DB_PASSWORD,
    DB_USERNAME
)

DB_URI= URL.create(
    drivername= DRIVERNAME,
    host= DB_HOSTNAME,
    username= DB_USERNAME,
    password= DB_PASSWORD,
    database= DB_NAME
)

engine= create_engine(DB_URI)
SessionLocal= sessionmaker(bind= engine)

# yield db connection
def get_db():
   try:
        db = SessionLocal()
        yield db
   finally:
        db.close()

# get self-closing db connection
class DatabaseSessionsManager:
    def __init__(self, url) -> None:
        engine= create_engine(url)
        session_local= sessionmaker(bind= engine)
        self.engine = session_local()

    def __enter__(self):
        return self.engine
        
    def __exit__(self, exc_type, exc_value, tb):
        self.engine.close()
