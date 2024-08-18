from sqlalchemy.orm import declarative_base
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker
from config.constants import settings

engine= create_engine(settings.pg_dsn.unicode_string())
SessionLocal= sessionmaker(bind= engine)


Base = declarative_base()

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
