from .models import Chat, Table
from .agent import agent

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login')
def home(request):
    logedin = True
    username = request.user.username
    chats = Chat.objects.all().order_by("datetime")
    items = Table.objects.all().order_by("date", "start_time")
    context = {'chats':chats, 'items':items, 'logedin': logedin, "username":username}
    return render(request, "base.html", context)

def input(request):
    user_input = request.POST["input"]
    ai_output = agent(user_input)
    chat = Chat(user=user_input, ai=ai_output)
    chat.save()
    return redirect("home")

def login_page(request):
    logedin = False
    chats = Chat.objects.all().order_by("datetime")
    items = Table.objects.all().order_by("date", "start_time")
    context = {'chats':chats, 'items':items, 'logedin': logedin}
    return render(request, "base.html", context)

@require_http_methods(["POST"])
def user_login(request):
    username=request.POST['username']
    password=request.POST['password']
    print(username, password)
    user=authenticate(request,username=username,password=password)
    print("ok")
    if user is not None:
        login(request, user)
        return redirect('home')
    else:
        logedin = False
        chats = Chat.objects.all().order_by("datetime")
        items = Table.objects.all().order_by("date", "start_time")
        contex = {'chats':chats, 'items':items, 'logedin': logedin,"msg": "Username or Password is incorrect 🚫"}
        return render(request, "base.html", contex)

def user_regiser(request):
    username=request.POST['username']
    email=request.POST['email']
    password=request.POST['password']
    user=User.objects.create_user(username, email, password)
    user.save()
    logedin = False
    chats = Chat.objects.all().order_by("datetime")
    items = Table.objects.all().order_by("date", "start_time")
    contex = {'chats':chats, 'items':items, 'logedin': logedin, "msg": "Registration successful ✅"}
    return render(request, "base.html", contex)

def user_logout(request):
    logout(request)
    return redirect('home')