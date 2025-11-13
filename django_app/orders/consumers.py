import json
from channels.generic.websocket import AsyncWebsocketConsumer

class OrderConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add("orders_group", self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({"message": "Conectado ao servidor WebSocket."}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("orders_group", self.channel_name)

    async def receive(self, text_data):
        pass

    async def send_new_order(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"]
        }))
