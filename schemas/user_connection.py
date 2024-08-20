from pydantic import BaseModel
from uuid import UUID

class ConnectionRequest(BaseModel):
    receiver_id: UUID

class RespondToRequest(BaseModel):
    response: str

class PendingRequestResponse(BaseModel):
    id: UUID
    sender_id: UUID
    status: str
