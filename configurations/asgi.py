"""
ASGI config for configurations project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

import django
# from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter,URLRouter
from django.core.asgi import get_asgi_application
from websocket_app.consumers import MessageConsumer
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configurations.settings')



django.setup()
# application = get_asgi_application()
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([
path("ws/<type>/<pk>/<token>/",MessageConsumer.as_asgi()),
        ])
})

# application=get_default_application()