from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from django.core import serializers
from .models import Chat, Table
from .agent import agent

# Create your views here.

def home(request):
    chats = Chat.objects.all().order_by("datetime")
    items = Table.objects.all()
    return render(request, "base.html", {'chats':chats, 'items':items})

def input(request):
    user_input = request.POST["input"]
    ai_output = agent(user_input)
    chat = Chat(user=user_input, ai=ai_output)
    chat.save()
    return redirect("home")
