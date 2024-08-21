from sqlalchemy import Boolean, Column, VARCHAR, TIMESTAMP, INTEGER
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from uuid import uuid4
from config.database_config import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(VARCHAR(25), unique=True, nullable=False)
    name = Column(VARCHAR(50), nullable=False)
    mobile = Column(VARCHAR, unique=True, nullable=False)
    email = Column(VARCHAR, unique=True, nullable=True)
    about = Column(VARCHAR, nullable=True)
    joined = Column(TIMESTAMP, default=datetime.now, nullable=False)

    # Flags
    is_active = Column(Boolean, default=True, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at = Column(TIMESTAMP, default=datetime.now, nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now, nullable=False)
    deleted_at = Column(TIMESTAMP, nullable=True)

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"

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

