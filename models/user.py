from sqlalchemy import Column, VARCHAR, TIMESTAMP, INTEGER
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from uuid import uuid4
from config.database_config import Base



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

class Conversation(Base):
    __tablename__ =  'conversation'
    id = Column(UUID(as_uuid= True), primary_key= True, default= uuid4)
    sender = Column(UUID(as_uuid= True))
    receiver = Column(UUID(as_uuid= True))
    message = Column(VARCHAR)
    sent_at = Column(TIMESTAMP)
    received_At = Column(TIMESTAMP)
    read_at = Column(TIMESTAMP)

