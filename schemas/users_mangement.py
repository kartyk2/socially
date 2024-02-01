from pydantic import BaseModel

class MobileLogin(BaseModel):
    phone: str

class ValidateOTP(BaseModel):
    phone: str
    otp: str


class UserDetails(BaseModel):
    username: str 
    name: str
    mobile: str
    email: str|None
    about: str|None

