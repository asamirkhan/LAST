import json

from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = 'notification'
        self.room_group_name = "notification_group"
        
        await(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.send(text_data=json.dumps({'status' : 'connected'}))
        
        
    async def receive(self, text_data):
        await self.send(text_data=json.dumps({'status' : 'success'}))


    async def disconnect(self , *args, **kwargs):
        print('disconnected')
    
	
    async  def send_notification(self , event):
        data = json.loads(event.get('value'))
        await self.send(text_data=json.dumps({'payload' : data}))