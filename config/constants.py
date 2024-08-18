from functools import lru_cache
from typing import Optional
from pydantic import PostgresDsn, RedisDsn, model_validator
from pydantic_settings import BaseSettings
from dotenv import dotenv_values
import os
from urllib.parse import quote

# Locate the .env file two levels up from the current script
current_script_path = os.path.abspath(__file__)
env_file_path = os.path.join(os.path.dirname(os.path.dirname(current_script_path)), '.env')

# Load environment variables
creds = dotenv_values(env_file_path)

class Settings(BaseSettings):
    # Twilio
    twilio_sid: str = creds.get('TWILIO_SID')
    auth_token: str = creds.get('AUTH_TOKEN')

    # Vonage
    api_secret: str = creds.get('API_SECRET')
    api_key: str = creds.get('API_KEY')

    # Redis
    redis_host: str = creds.get('REDIS_HOST')
    redis_port: int = int(creds.get('REDIS_PORT'))
    redis_dsn: Optional[RedisDsn] = None

    # PostgreSQL
    db_driver: str = creds.get('DRIVER_NAME')
    db_hostname: str = creds.get('DB_HOSTNAME')
    db_port: int = int(creds.get('DB_PORT'))
    db_username: str = creds.get('DB_USERNAME')
    db_password: str = creds.get("DB_PASSWORD")
    db_name: str = creds.get('DB_NAME')
    pg_dsn: Optional[PostgresDsn] = None

    # Encryption
    encoding_secret_key: str = creds.get("ENCODING_SECRET_KEY")
    encoding_algorithm: str = creds.get("ENCODING_ALGORITHM", "HS256")

    # Helper function to encode the password
    def encode_password(self, password: str) -> str:
        return quote(password, safe='')

    # Combined validator for both Redis and PostgreSQL DSNs
    @model_validator(mode='after')
    def assemble_dsns(self) -> 'Settings':
        if not self.redis_dsn:
            self.redis_dsn = RedisDsn.build(
                scheme='redis',
                host=self.redis_host,
                port=self.redis_port,
                path='/0'
            )
        
        if not self.pg_dsn:
            encoded_password = self.encode_password(self.db_password)
            self.pg_dsn = PostgresDsn.build(
                scheme=self.db_driver,
                username=self.db_username,
                password=encoded_password,
                host=self.db_hostname,
                port=self.db_port,
                path=f"{self.db_name or ''}"
            )
        
        return self

# Caching the settings instance
@lru_cache
def get_settings():
    return Settings()

# Example usage
settings = get_settings()
