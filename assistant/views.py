from django.shortcuts import render, redirect
from .models import Chat, Table
from django.core import serializers
from .agent import agent

# Create your views here.

# def check(items):
#     items_json = serializers.serialize('json', items)
#     print(items_json)
    

def home(request):
    chats = Chat.objects.all().order_by("datetime")
    items = Table.objects.all()
    # check(items)
    return render(request, "base.html", {'chats':chats, 'items':items})

def input(request):
    user_input = request.POST["input"]
    ai_output = agent(user_input)
    chat = Chat(user=user_input, ai=ai_output)
    chat.save()
    return redirect("home")
