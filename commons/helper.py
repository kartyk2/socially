import jwt
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
from config.constants import get_settings
from config.database_config import get_db
from models.user import User

security = HTTPBearer()
settings= get_settings()

class TokenPayload(BaseModel):
    id: str
    username: str
    exp: datetime

def decode_jwt(token: str, secret_key: str) -> TokenPayload:
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return TokenPayload(**payload)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
    secret_key: str = Depends(lambda: settings.encoding_secret_key)
) -> User:
    token = credentials.credentials
    token_data = decode_jwt(token, secret_key)
    
    user = db.query(User).filter(User.id == token_data.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
