from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.exceptions import AcceptConnection,DenyConnection
from asgiref.sync import async_to_sync


# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = "chat_{}".format(self.room_name)
#         async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
#         # self.accept()这里可以做逻辑判断  基站与后台连接时,如果没有标识码(与周文豪协商)  就不accept  这样连接直接中断
#         # accept一般是放在connect函数的最后的
#         self.accept()
#
#     def disconnect(self, close_code):
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )
#
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )
#
#     def chat_message(self, event):
#         message = event['message']
#
#         # Send message to WebSocket
#         self.send(text_data=json.dumps({
#             'message': message
#         }))

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                # type 是一个事件函数 的名称
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    # 自定义的事件函数名称
    async def chat_message(self, event):
        # event["message"] 即为上面的 74行的message
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))