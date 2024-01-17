from dotenv import dotenv_values
import os 

current_script_path = os.path.abspath(__file__)

# Navigate two levels up to find the .env file
env_file_path = os.path.join(os.path.dirname(os.path.dirname(current_script_path)), '.env')

creds= dotenv_values(env_file_path)

TWILIO_SID= creds.get('TWILIO_SID')
AUTH_TOKEN= creds.get('AUTH_TOKEN')

