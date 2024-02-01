from fastapi import FastAPI, WebSocket
from fastapi.encoders import jsonable_encoder
from routers.user_management import user_manager
from config.constants import AUTH_TOKEN, TWILIO_SID
from config.database_config import engine
from models.models import Base
import json

app = FastAPI(title= "Socially")
app.include_router(user_manager)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    acceptence= await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"You sent: {data}")


# @app.on_event('startup')
# async def startup():
#     Base.metadata.create_all(bind= engine)