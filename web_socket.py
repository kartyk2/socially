from socketio import AsyncClient
import socketio

socket_server= socketio.AsyncServer()

socket_app= socketio.ASGIApp(socket_server, socketio_path='ws')

@socket_server.event
async def connect(sid, environ, auth):
    print(f'{sid}: connected')
    await socket_server.emit('join', {'sid': sid})


@socket_server.event
async def chat(sid, message):
    await socket_server.emit('chat', {'sid': sid, 'message': message})


@socket_server.event
async def disconnect(sid):
    print(f'{sid}: disconnected')