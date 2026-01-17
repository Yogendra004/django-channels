import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class TestConsumer(WebsocketConsumer):
    def connect(self):
        print("WebSocket connect called")
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
