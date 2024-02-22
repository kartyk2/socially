from pydantic import BaseModel, Field
from uuid import UUID

class MobileLogin(BaseModel):
    phone: str

class ValidateOTP(BaseModel):
    phone: str
    otp: str

class Mobile(BaseModel):
    internantional_code: str = '+91'
    number: str 

class UserDetails(BaseModel):
    username: str = Field(..., pattern="^[a-z0-9_.]+$", description="Non-breaking one-word string", examples=["ostvinden"])
    name: str
    mobile: str
    email: str|None = None
    about: str|None = None

class Message(BaseModel):
    sender: UUID
    receiver: UUID
    text: str
