from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from schemas.users_mangement import MobileLogin, ValidateOTP
from random import randint
from datetime import datetime, timedelta
import vonage
  
from config.constants import API_KEY, API_SECRET
from config.log_config import Logger
from config.redis_config import redis_client

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
            redis_client.setex(name=mobile_login.phone, value=otp, time= timedelta(seconds=30))
            logger.info(f"Message sent successfully to {mobile_login.phone}.")
        else:
            logger.info(f"Message failed with error: {responseData['messages'][0]['error-text']}")
            return JSONResponse(status_code=500, content= "Failed to send OTP")

    except Exception as error:
        logger.info(error)


@user_manager.post('/validate_otp')
async def mobile_login(opt_details: ValidateOTP):
    
    try:
        set_otp= redis_client.get(opt_details.phone)
        if set_otp is None:
            logger.info("reached OTP request for unset mobile number")
            return JSONResponse(content= "Please request for otp first", status_code= 400)
            

        if set_otp == opt_details.otp:
            """
            """

    except Exception as error:
        logger.info(error)
 