import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class TestConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = "test_consumer"
        self.room_group_name = "test_consumer_group"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()
        self.send(text_data=json.dumps({"status": "connected"}))

    def receive(self, text_data=None, bytes_data=None):
        print(f"Message received: {text_data}")
        if text_data:
            self.send(text_data=json.dumps({"echo": text_data}))

    def disconnect(self, close_code):
        print(f"WebSocket disconnected with code {close_code}")
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        self.send(text_data=json.dumps({"echo": "disconnected"}))

    def send_notification(self, event):
        data = json.loads(event.get("value"))
        self.send(text_data=json.dumps({"payload": data}))


class NewTestConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.room_name = "new_consumer"
        self.room_group_name = "new_consumer_group"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({"status": "connected from async server"}))

    async def receive(self, text_data=None, **kwargs):
        if text_data:
            await self.send(text_data=json.dumps({"echo": text_data}))

    async def disconnect(self, code):
        print(f"WebSocket disconnected with code {code}")
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def send_async_notifications(self, event):
        data = json.loads(event.get("value"))
        await self.send(text_data=json.dumps({"payload": data}))
