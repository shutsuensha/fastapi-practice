from fastapi.websockets import WebSocket
from datetime import datetime


class WebSocketManager:
    def __init__(self):
        self.connected_clients = []


    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connected_clients.append(websocket)
        client_ip = f"{websocket.client.host}:{websocket.client.port}"
        message = {"client":client_ip,"message": f"Welcome {client_ip}"}
        await websocket.send_json(message)


    async def send_message(self, websocket: WebSocket, message: dict):
        message = {
            "client": message['client'],
            "message": message['content'],
            "timestamp":message['timestamp']
        }

        await websocket.send_json(message)


    async def disconnect(self, websocket: WebSocket):
        self.connected_clients.remove(websocket)
