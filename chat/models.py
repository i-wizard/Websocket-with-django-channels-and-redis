from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Thread(models.Model):
    first = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_thread_first_name')
    second = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_thread_second_name')
    timestamp = models.DateTimeField(auto_now_add=True)

class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)