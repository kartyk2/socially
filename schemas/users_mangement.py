from pydantic import BaseModel

class MobileLogin(BaseModel):
    phone: str