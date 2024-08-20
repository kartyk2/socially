import enum
import uuid
from sqlalchemy import Column, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from config.database_config import Base

from models.user import User


class ConnectionStatus(enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    BLOCKED = "blocked"

class Connection(Base):
    __tablename__ = 'connections'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id), nullable=False)
    connected_user_id = Column(UUID(as_uuid=True), ForeignKey(User.id), nullable=False)
    status = Column(Enum(ConnectionStatus), nullable=False, default=ConnectionStatus.PENDING)
    