import os
import logging
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from home.consumers import TestConsumer

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from home.consumers import TestConsumer
from django.core.asgi import get_asgi_application
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": URLRouter(
            [
                path("ws/test/", TestConsumer.as_asgi()),  # exact match
            ]
        ),
    }
)
