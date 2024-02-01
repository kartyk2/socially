from fastapi import Depends, status
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from schemas.users_mangement import MobileLogin, ValidateOTP
from random import randint
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from models.models import User, UserActivity
  
from config.database_config import get_db
from config.constants import API_KEY, API_SECRET, ENCODING_SECRET_KEY
from config.log_config import Logger
from config.redis_config import redis_client
import vonage, jwt, traceback

logger= Logger().get_logger()
user_manager = APIRouter()
client = vonage.Client(key=API_KEY, secret=API_SECRET)


@user_manager.post('/mobile_login')
async def mobile_login(mobile_login: MobileLogin):
    otp= randint(10000, 999999)
    
    try:
        if redis_client.get(mobile_login.phone):
            return JSONResponse(content= "Please wait for 30 seconds before requesting another otp", status_code= 429)
            
        responseData = client.sms.send_message(
            {
                "from": "Socially",
                "to": mobile_login.phone,
                "text": f"You OTP for Socially login is {otp}. Stay safe.",
            }
        )
        if responseData["messages"][0]["status"] == "0":
            redis_client.setex(name=mobile_login.phone, value=otp, time= timedelta(minutes=10))
            logger.info(f"Message sent successfully to {mobile_login.phone}.")
        else:
            logger.info(f"Message failed with error: {responseData['messages'][0]['error-text']}")
            return JSONResponse(status_code=500, content= "Failed to send OTP")

    except Exception as error:
        logger.info(traceback.format_exc())


@user_manager.post('/validate_otp')
async def validate_otp(otp_details: ValidateOTP , db: Session = Depends(get_db)):
    
    try:
        set_otp= redis_client.get(otp_details.phone)
        if set_otp is None:
            logger.info("reached OTP request for unset mobile number")
            return JSONResponse(content= "Please request for otp first", status_code= 400)

        if set_otp == otp_details.otp:
            """
            check if the user is already signed up
            """
            returning_user= db.query(User).filter(User.mobile == otp_details.phone).with_entities(User.id, User.username).first()
            if returning_user:
                """
                    return the access token and the id for the user
                """
                access_token_payload= {
                    "id": returning_user.id,
                    "username": returning_user.username,
                    "exp": datetime.now() + timedelta(hours= 2)    
                }
                
                response= {
                    "user_registered": True,
                    "user": returning_user,
                    "access_token": jwt.encode(access_token_payload, key= ENCODING_SECRET_KEY)
                }

                return JSONResponse(content= response)
                
            else:
                response= {
                    "user_registered": False,
                    "phone": otp_details.phone
                }
          
                return JSONResponse(content= response)
                
    except Exception as error:
        logger.info(traceback.format_exc())


# @user_manager.post('/register_user')
# async def register_user(user_details: UserDetails , db: Session = Depends(get_db)):
#     """
#     """