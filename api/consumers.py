
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Chat ,MessagesUser
from django.contrib.auth.models import User 


class ChatingConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.group_name = self.scope['url_route']['kwargs']['gname']
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

    def receive(self , text_data):
        self.data_json = json.loads(text_data)
        # print(self.data_json)
        self.chatobj = Chat.objects.get(msgRoomid = self.data_json['chatid'])
        self.msg_value = {
            'senderuser':User.objects.get(username=self.data_json['senderuser']),
            'recieveuser':User.objects.get(username= self.data_json['recieveuser']),
            'textmessage':self.data_json['textmessage'],
        }
        self.msg_obj = MessagesUser.objects.create(**self.msg_value)
        self.msg_obj.save()
        self.id = self.msg_obj.id
        self.msgobj = MessagesUser.objects.get(id=self.id)

        self.chatobj.msg.add(self.msgobj)
        self.chatobj.save()

        self.message = self.data_json['textmessage']
        self.user = self.data_json['senderuser']
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,{
                'type':'chat_message',
                'message':self.message,
                'senderuser':self.user

            }
        )
    
    def chat_message(self , event):
        self.message = event['message']
        self.user = event['senderuser']
        self.send(text_data = json.dumps({
            'type':'chat',
            'message':self.message,
            'senderuser':self.user

        }))

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()
        self.room_group_name ='test'
        print(" Room ID:      " ,self.scope['url_route']['kwargs']['gname'])
        self.groupname = self.scope['url_route']['kwargs']['gname']
        async_to_sync(self.channel_layer.group_add)(
            self.groupname,
            self.channel_name,
        )
        self.send(text_data = json.dumps({
            'type':'connection-established',
            'message':"hello there",
        }))

    def receive(self , text_data):

        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print('message' ,message)


        async_to_sync(self.channel_layer.group_send)(
            self.groupname,{
                'type':'chat_message',
                'message':message,
            }
        )
    def chat_message(self , event):
        message = event['message']
        self.send(text_data = json.dumps({
            'type':'chat',
            'message':message
        }))
        # self.send(text_data = json.dumps({
        #     'type':'chat',
        #     'message':message,
        # }))
        