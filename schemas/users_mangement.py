from pydantic import BaseModel

class MobileLogin(BaseModel):
    phone: str

class ValidateOTP(BaseModel):
    phone: str
    otp: str