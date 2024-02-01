from sqlalchemy import Column, VARCHAR, TIMESTAMP, INTEGER
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True)
    username = Column(VARCHAR)
    name = Column(VARCHAR)
    mobile = Column(VARCHAR)
    email = Column(VARCHAR)
    about = Column(VARCHAR)
    joined = Column(TIMESTAMP, default= datetime.now())

class UserActivity(Base):
    __tablename__ = 'user_activity'
    user_id = Column(UUID(as_uuid=True), primary_key=True)
    last_seen = Column(TIMESTAMP)