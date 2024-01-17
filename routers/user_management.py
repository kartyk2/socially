from fastapi.routing import APIRouter
from schemas.users_mangement import MobileLogin
from twilio.rest import Client
from random import randint

from config.constants import TWILIO_SID, AUTH_TOKEN
from config.log_config import Logger

logger= Logger().get_logger()
user_manager = APIRouter()
client = Client(TWILIO_SID, AUTH_TOKEN)


@user_manager.post('/mobile_login')
async def mobile_login(mobile_login: MobileLogin):
    
    """
    """
    otp= randint(10000, 999999)
    
    
    try:
        message = client.messages.create(
            to=mobile_login.phone,
            from_="+12293514890",
            body=f"You OTP for Socially login is {otp}. Stay safe (❁´◡`❁)")
    except Exception as twilio_exception:
        logger.info(twilio_exception)
