from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Chat(models.Model):
    datetime = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    user_text = models.CharField(max_length=500)
    ai_text = models.CharField(max_length=1000, blank=True)

class Table(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    user = models.CharField(max_length=50)
    topic = models.CharField(max_length=500)
