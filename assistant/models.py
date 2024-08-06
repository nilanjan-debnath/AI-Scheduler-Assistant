from django.db import models

# Create your models here.

class Chat(models.Model):
    datetime = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.CharField(max_length=500)
    ai = models.CharField(max_length=1000, blank=True)

class Table(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    user_name = models.CharField(max_length=50)
    topic = models.CharField(max_length=500)
