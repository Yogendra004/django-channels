import asyncio
from django.shortcuts import render
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create your views here.
import time
from django.http import JsonResponse


async def home(request):

    for i in range(1, 10):
        channel_layer = get_channel_layer()
        data = {"count": i}
        await channel_layer.group_send(
            "new_consumer_group",
            {"type": "send_async_notifications", "value": json.dumps(data)},
        )
        # time.sleep(1)

    return render(request, "home.html")


def generate_students(request):
    from .thread import CreateStudentThread

    total = request.GET.get("total")

    thread = CreateStudentThread(int(total))
    thread.start()

    return JsonResponse({"status": 200})
