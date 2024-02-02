from fastapi import FastAPI, WebSocket
from fastapi.encoders import jsonable_encoder
from sqlalchemy import text
from routers.user_management import user_manager
from config.constants import AUTH_TOKEN, TWILIO_SID
from config.database_config import engine, DB_URI, DatabaseSessionsManager
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
#     #drop all tables
#     with DatabaseSessionsManager(DB_URI) as db:
#         db.execute(text(
#             """
#             DROP SCHEMA public CASCADE;
#             CREATE SCHEMA public;

#             GRANT ALL ON SCHEMA public TO postgres;
#             """
#         ))
#         db.commit()
        
#     #create all user defined tables
#     Base.metadata.create_all(bind= engine)