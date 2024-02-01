from dotenv import dotenv_values
import os 

current_script_path = os.path.abspath(__file__)

# Navigate two levels up to find the .env file
env_file_path = os.path.join(os.path.dirname(os.path.dirname(current_script_path)), '.env')

creds= dotenv_values(env_file_path)

#Twilio
TWILIO_SID= creds.get('TWILIO_SID')
AUTH_TOKEN= creds.get('AUTH_TOKEN')

#Vonage
API_SECRET= creds.get("API_SECRET")
API_KEY= creds.get("API_KEY")

#Redis
REDIS_PORT= creds.get("REDIS_PORT")
REDIS_HOST= creds.get("REDIS_HOST")

#database
DRIVERNAME= creds.get("DRIVER_NAME")
DB_HOSTNAME= creds.get("DB_HOSTNAME")
DB_USERNAME= creds.get("DB_USERNAME") 
DB_PASSWORD= creds.get("DB_PASSWORD")
DB_NAME= creds.get("DB_NAME")

#keys
ENCODING_SECRET_KEY= creds.get("SECRET_KEY")