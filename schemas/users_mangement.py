from pydantic import BaseModel, Field
from uuid import UUID

class Mobile(BaseModel):
    internantional_code: str = '+91'
    number: str = Field(..., pattern= "^[0-9]{10}$")

class ValidateOTP(BaseModel):
    phone: str
    otp: str


class UserDetails(BaseModel):
    username: str = Field(..., pattern="^[a-z0-9_.]+$", description="Non-breaking one-word string", examples=["ostvinden"])
    name: str
    mobile: str
    email: str | None = None
    about: str | None = None

class Message(BaseModel):
    sender: UUID
    receiver: UUID
    text: str
