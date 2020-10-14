import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.db.models import Q

from .models import ChatMessage, Thread

class ChatConsumer(AsyncConsumer):
    # on page load it  gets the current thread and creates the chatroom
    async def websocket_connect(self, event):
        print('connected: ',  event)
        await asyncio.sleep(1)
        other_user = self.scope['url_route']['kwargs']['username']
        me = self.scope['user']
        thread_obj = await self.get_thread(me, other_user)
        self.thread_obj = thread_obj
        print('thread: ', thread_obj)
        chat_room = f"thread_{thread_obj.id}"
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room, self.channel_name
        )
        await self.send({
            'type':'websocket.accept'
        })
    #this view gets the msg from the frontend and call the fxn to create chat msg and decides which chat roo the msg should go
    async def websocket_receive(self, event):
        print('received: ',  event)
        json_data = event.get('text', None)
        if json_data is not None:
            text_dict = json.loads(json_data) #json.loads turns a string received from the frontend into a dictionary
            msg = text_dict.get('msg')
            print('msg: ', msg)
            user = self.scope['user']
            username = ' anonymous'
            if user.is_authenticated:
                username = user.username
            finalData = {
                'message':msg,
                'username':username
            }
            await self.create_chat_msg(msg)
            #this broadcast the event that contains the message
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    'type': 'chat_message',
                    'text':json.dumps(finalData) #this is to convert the dictionary to string 
                }
            )
    async def chat_message(self, event):
        #sends the actual message
        await self.send({
            'type':'websocket.send',
            'text':event['text']
        })
        # print('message: ', event)
    async def websocket_disconnect(self, event):
        print('disconnected: ',  event)
    @database_sync_to_async
    def get_thread(self, user, other_username):
        qlookup1 = Q(first__username=user.username) & Q(second__username=other_username)
        qlookup2 = Q(first__username=other_username) & Q(second__username=user.username)
        thread = Thread.objects.filter(qlookup1 | qlookup2).first()
        return thread
    @database_sync_to_async
    def create_chat_msg(self, msg):
        thread_obj = self.thread_obj
        me = self.scope['user']
        return ChatMessage.objects.create(thread=thread_obj, user=me, message=msg)