from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import func, or_
from sqlalchemy.orm import Session
from config.constants import settings
from config.database_config import get_db
from config.clients import redis_client, sms_client
from config.log_config import Logger
from models import User
from schemas.users_mangement import Mobile, UserDetails, ValidateOTP
import jwt
from random import randint
from datetime import datetime, timedelta

user_manager = APIRouter()

# Define loggers
error_logger = Logger.get_error_logger()
info_logger = Logger.get_api_info_logger()
success_logger = Logger.get_success_logger()

class UserManager:
    def __init__(self, db: Session):
        self.db = db

    def check_user_exists(self, phone: str):
        return self.db.query(User).filter(User.mobile == phone).first()

    def send_otp(self, phone: str, otp: int):
        response = sms_client.sms.send_message(
            {
                "from": "Socially",
                "to": phone,
                "text": f"Your OTP for Socially login is {otp}. Stay safe.",
            }
        )
        return response

    def validate_otp(self, phone: str, otp: str):
        stored_otp = redis_client.get(phone)
        return stored_otp is not None and stored_otp == otp

    def register_user(self, user_details: UserDetails):
        new_user = User(**user_details.dict(exclude_unset=True, exclude_defaults=True, exclude_none=True))
        self.db.add(new_user)
        self.db.commit()
        return new_user

    def find_users(self, keyword: str):
        filters = [
            func.lower(User.username).like(f'%{keyword.lower()}%'),
            func.lower(User.name).like(f'%{keyword.lower()}%')
        ]
        return self.db.query(User).filter(or_(*filters)).all()

@user_manager.post('/mobile_login')
async def mobile_login(mobile_login: Mobile, db: Session = Depends(get_db)):
    user_manager = UserManager(db)
    otp = randint(100000, 999999)
    
    # Check if user exists
    if not user_manager.check_user_exists(mobile_login.number):
        info_logger.info(f"OTP request denied for non-existing user with phone {mobile_login.number}.")
        return JSONResponse(
            content="User does not exist.",
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    # Check rate limit in Redis
    if redis_client.get(mobile_login.number):
        info_logger.info(f"OTP request denied for {mobile_login.number} due to recent request.")
        return JSONResponse(
            content="Please wait for 30 seconds before requesting another OTP",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS
        )
    
    try:
        response_data = user_manager.send_otp(mobile_login.internantional_code+mobile_login.number, otp)
        info_logger.info(f"SMS response for {mobile_login.number}: {response_data}")

        if response_data["messages"][0]["status"] == "0":
            redis_client.setex(name=mobile_login.number, value=otp, time=timedelta(minutes=10))
            success_logger.info(f"OTP sent successfully to {mobile_login.number}.")
            return JSONResponse(
                content="OTP sent successfully.",
                status_code=status.HTTP_200_OK
            )
        else:
            error_logger.error(f"Failed to send OTP to {mobile_login.number}. Error: {response_data['messages'][0]['error-text']}")
            return JSONResponse(
                content="Failed to send OTP.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    except Exception as e:
        error_logger.error(f"Error occurred while sending OTP to {mobile_login.number}: {str(e)}")
        return JSONResponse(
            content="An internal error occurred. Please try again later.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@user_manager.post('/validate_otp')
async def validate_otp(otp_details: ValidateOTP, db: Session = Depends(get_db)):
    user_manager = UserManager(db)
    try:
        if not user_manager.validate_otp(otp_details.phone, otp_details.otp):
            info_logger.info(f"OTP validation failed for {otp_details.phone}: Incorrect OTP.")
            return JSONResponse(
                content="Invalid OTP.",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        returning_user = user_manager.check_user_exists(otp_details.phone)
        if returning_user:
            access_token_payload = {
                "id": returning_user.id.__str__(),
                "username": returning_user.username,
                "exp": datetime.utcnow() + timedelta(hours=2)
            }
            token = jwt.encode(access_token_payload, key=settings.encoding_secret_key)
            success_logger.info(f"OTP validated successfully for {otp_details.phone}. Returning user.")
            return JSONResponse(
                content={"user_registered": True, "user": returning_user.username, "access_token": token},
                status_code=status.HTTP_200_OK
            )
        else:
            success_logger.info(f"OTP validated successfully for {otp_details.phone}. New user.")
            return JSONResponse(
                content={"user_registered": False, "phone": otp_details.phone},
                status_code=status.HTTP_200_OK
            )
    
    except Exception as e:
        error_logger.error(f"Error occurred during OTP validation for {otp_details.phone}: {str(e)}")
        return JSONResponse(
            content="An internal error occurred. Please try again later.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@user_manager.post('/register_user')
async def register_user(user_details: UserDetails, db: Session = Depends(get_db)):
    user_manager = UserManager(db)
    try:
        new_user = user_manager.register_user(user_details)
        success_logger.info(f"New user registered: {user_details.username}")
        return JSONResponse(
            content={"user_registered": True, "user_created": user_details.username},
            status_code=status.HTTP_201_CREATED
        )
    
    except Exception as e:
        error_logger.error(f"Error occurred while registering user {user_details.username}: {str(e)}")
        return JSONResponse(
            content="An internal error occurred. Please try again later.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@user_manager.get('/find_users')
async def find_users(keyword: str, db: Session = Depends(get_db)):
    user_manager = UserManager(db)
    try:
        users = user_manager.find_users(keyword)
        info_logger.info(f"Users found with keyword '{keyword}': {len(users)}")
        return users

    except Exception as e:
        error_logger.error(f"Error occurred during user search with keyword '{keyword}': {str(e)}")
        return JSONResponse(
            content="An internal error occurred. Please try again later.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
