from fastapi import WebSocket
import socketio
import asyncio

sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=["*"]
)

sio_app = socketio.ASGIApp(sio, socketio_path='sockets')


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket, ):
        """
        Add the current websocket connection to user- socket mapping 
        """
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


websocket_manager = ConnectionManager()