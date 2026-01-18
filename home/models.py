from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json


class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.CharField(max_length=500)
    is_seen = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        channel_layer = get_channel_layer()
        notification_objs = Notifications.objects.filter(is_seen=False).count()
        data = {"count": notification_objs, "current_notification": self.notification}
        async_to_sync(channel_layer.group_send)(
            "test_consumer_group",
            {"type": "send_notification", "value": json.dumps(data)},
        )
        super(Notifications, self).save(*args, **kwargs)

    def __str__(self):
        return f"notifications for {self.user.username} is called"
