from sqlalchemy import Column, VARCHAR, TIMESTAMP, INTEGER
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from uuid import uuid4

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default= uuid4)
    username = Column(VARCHAR(25), unique= True)
    name = Column(VARCHAR(50))
    mobile = Column(VARCHAR, unique= True)
    email = Column(VARCHAR, unique= True)
    about = Column(VARCHAR)
    joined = Column(TIMESTAMP, default= datetime.now())

class UserActivity(Base):
    __tablename__ = 'user_activity'
    user_id = Column(UUID(as_uuid=True), primary_key=True)
    last_seen = Column(TIMESTAMP)