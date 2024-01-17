from fastapi import FastAPI, WebSocket
from routers.user_management import user_manager

from config.constants import AUTH_TOKEN, TWILIO_SID

app = FastAPI()
app.include_router(user_manager)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(data)
        await websocket.send_text(f"You sent: {data}")