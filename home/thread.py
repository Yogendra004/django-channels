import threading
import json
import time
import random
from .models import *
from faker import Faker
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

fake = Faker()


class CreateStudentThread(threading.Thread):
    def __init__(self, total):
        self.total = total
        threading.Thread.__init__(self)

    def run(self):
        try:
            print("Thread execution started")
            channel_layer = get_channel_layer()
            current_total = 0
            for i in range(self.total):
                current_total += 1
                student_obj = Students.objects.create(
                    student_name=fake.name(),
                    student_email=fake.email(),
                    address=fake.address(),
                    age=random.randint(10, 50),
                )
                data = {
                    "id": current_total,
                    "student_name": student_obj.student_name,
                    "student_email": student_obj.student_email,
                    "address": student_obj.address,
                    "student_age": student_obj.age,
                    "total": self.total,
                    "current_total": current_total,
                }
                print({"data": data})
                async_to_sync(channel_layer.group_send)(
                    "new_consumer_group",
                    {"type": "send_async_notifications", "value": json.dumps(data)},
                )
                time.sleep(1)  # Add delay between messages
        except Exception as e:
            print(f"Error in thread execution: {e}")
        print("Thread execution ended")
