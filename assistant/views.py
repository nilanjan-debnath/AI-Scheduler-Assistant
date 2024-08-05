from django.shortcuts import render, redirect
from .models import Chat, Table

# Create your views here.

def home(request):
    chats = Chat.objects.all().order_by("datetime")
    return render(request, "base.html", {'chats':chats})

def input(request):
    user = request.POST["input"]
    chat = Chat(user=user)
    chat.save()
    return redirect("home")
