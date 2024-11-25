from channels.generic.websocket import AsyncJsonWebsocketConsumer

class DrawConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = "draw_room"
        self.room_group_name = f"draw_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive_json(self, content):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "broadcast_draw_data",
                "data": content,  
            }
        )

    async def broadcast_draw_data(self, event):

        await self.send_json(event["data"])
