import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import requests

backend_base_url="http://localhost:8000/"
# url_for_check_permission_on_suuport=f"{backend_base_url}support/check-permission/"
url_for_check_permission_on_support=None
url_for_send_message_on_support=None

# url_for_check_permission_on_chat=f"{backend_base_url}chat/check-permission/"
url_for_check_permission_on_chat=None
url_for_send_message_on_chat=None


class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # print(self.scope['url_route'])
        self.room_pk = self.scope['url_route']['kwargs']['pk']
        self.room_type = self.scope['url_route']['kwargs']['type']
        self.room_group_name = self.room_type+self.room_pk
        self.token = self.scope['url_route']['kwargs']['token']
        self.data={}
        if self.room_type=="event":
            await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )
            await self.channel_layer.group_send(
                    self.room_group_name,
                    {"type":"connected_message",
                        "data":self.data,
                        }
                )
            self.accept()
        elif self.room_type=="chat":
            if url_for_check_permission_on_chat:
                url=f"{url_for_check_permission_on_chat}?pk={self.room_pk}"
                try:
                    res=requests.get(url,headers={
                        "Authorization":f"Token {self.token}"
                    })
                except:
                    self.permission=False
                self.data=json.loads(res.text)["data"]
                self.permission=self.data["permission"]
                
                permission=self.permission
                if permission:
                    await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )
                    await self.accept()
                    await self.channel_layer.group_send(
                    self.room_group_name,
                    {"type":"connected_message",
                        "data":self.data,
                        }
                )
                else:
                    await self.close()
                
                
            else:
                self.data={"id":self.token}
                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {"type":"connected_message",
                        "data":self.data,
                        }
                )
                await self.accept()

        elif self.room_type=="support":
        # Join room group
            if url_for_check_permission_on_support:
                url=f"{url_for_check_permission_on_support}?pk={self.room_pk}"
                try:
                    res=requests.get(url,headers={
                        "Authorization":f"Token {self.token}"
                    })
                except:
                    self.permission=False
                self.data=json.loads(res.text)["data"]
                self.permission=self.data["permission"]
                
                permission=self.permission
                if permission:
                    await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )
                    await self.accept()
                    await self.channel_layer.group_send(
                    self.room_group_name,
                    {"type":"connected_message",
                        "data":self.data,
                        }
                )
                else:
                    await self.close()
            else:
                self.data={"id":self.token}
                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {"type":"connected_message",
                        "data":self.data,
                        }
                )
                await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type":"disconnected_message",
                "message":json.dumps(self.data),
                }
        )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        if self.room_type=="support" and url_for_send_message_on_support:
            # url=f"{backend_base_url}support/sent-message/"
            requests.post(url_for_send_message_on_support,
                          data={"text":text_data,
                                "chat":self.room_pk},headers={
                    "Authorization":f"Token {self.token}"
                })
        elif self.room_type=="chat" and url_for_send_message_on_chat:
            requests.post(url_for_send_message_on_support,
                          data={"text":text_data,
                                "chat":self.room_pk},headers={
                    "Authorization":f"Token {self.token}"
                })
        # elif self.room_type=="event":
        #     pass
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type":"send_message",
                "message":text_data,
                "data":self.data
                }
        )


    async def send_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def connected_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def disconnected_message(self, event):
        await self.send(text_data=json.dumps(event))