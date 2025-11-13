import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
import asyncio
import redis

class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("orders_group", self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({"message": "Conectado ao servidor WebSocket."}))

        asyncio.create_task(self.listen_to_redis())

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("orders_group", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            "orders_group",
            {"type": "send_order", "message": data.get("message", "")}
        )

    async def send_order(self, event):
        await self.send(text_data=json.dumps({"message": event["message"]}))

    async def listen_to_redis(self):
        r = redis.Redis(host='127.0.0.1', port=6379)
        pubsub = r.pubsub()
        pubsub.subscribe('orders_channel')

        for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])
                msg = f" Novo pedido recebido! ID: {data['id']} | Produto: {data['product']} | Valor: R$ {data['value']}"
                await self.channel_layer.group_send(
                    "orders_group",
                    {"type": "send_order", "message": msg}
                )
