from django.urls import re_path ,path

from . import consumers

websocket_urlpatterns = [
    # path(r'ws/socket-server/<str:gname>/' , consumers.ChatConsumer.as_asgi()),
    path(r'ws/chat-server/<str:gname>/' , consumers.ChatingConsumer.as_asgi()),

]