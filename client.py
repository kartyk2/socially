import socketio, asyncio

socket_client = socketio.AsyncClient()


@socket_client.event
def connect():
    print(f"I'm connected! with SID: {socket_client.sid}")


@socket_client.event
def connect_error():
    print("The connection failed!")


@socket_client.event
def disconnect():
    print(f"I'm disconnected!{socket_client.sid}")


async def main():
    await socket_client.connect("http://localhost:8000", socketio_path="/sockets")
    print("HEHE")
    await socket_client.disconnect()


async def run_main():
    await main()


asyncio.run(main())
