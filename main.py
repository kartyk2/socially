from fastapi import FastAPI
from routers.user_management import user_manager
from config.log_config import Logger

from config.websocket_config import sio_app

app = FastAPI(title="Socially")
app.mount("/", sio_app)

app.include_router(user_manager)
logger = Logger().get_logger()
