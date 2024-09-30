import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        room = await self.get_room()  # Fetch the room object

        # Check if the room is full
        print(f"Current Members: {room.current_members}, Max Members: {room.max_members}")
        if room.current_members >= room.max_members:
            print("Room is full. Rejecting connection.")
            await self.close()  # Reject the connection if the room is full
            return

        await self.channel_layer.group_add(self.room_name, self.channel_name)
    
        # Increment the current members count
        await self.increment_member_count(room)

        await self.accept()

    @database_sync_to_async
    def get_room(self):
        return Room.objects.select_for_update().get(room_name=self.room_name)

    @database_sync_to_async
    def increment_member_count(self, room):
        room.current_members += 1
        room.save()

    async def disconnect(self, code):
        room = await self.get_room()  # Fetch the room object
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
        await self.decrement_member_count(room)  # Decrease the count on disconnect
        await self.close(code)

    @database_sync_to_async
    def decrement_member_count(self, room):
        if room.current_members > 0:
            room.current_members -= 1
            room.save()


    async def receive(self, text_data):
        data_json = json.loads(text_data)

        event = {
            "type" : "send_message",
            "message" : data_json,
        }

        await self.channel_layer.group_send(self.room_name, event)
    
    async def send_message(self, event):
        data = event["message"]
        await self.create_message(data = data)

        response = {
            "sendman":data["sendman"],
            "message":data["message"],
        }

        await self.send(text_data=json.dumps({"message":response}))
    
    @database_sync_to_async
    def create_message(self, data):
        get_room = Room.objects.get(room_name=data['room_name'])
        if not Message.objects.filter(message=data['message'], sender=data["sendman"]).exists():
            new_message = Message.objects.create(room=get_room, message=data["message"], sender=data["sendman"])
