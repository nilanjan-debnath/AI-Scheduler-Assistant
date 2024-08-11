from .models import Chat, Table
from .agent import agent

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.
msg = ""

@login_required(login_url='login')
def home(request):
    global msg
    msg = ""
    logedin = True
    username = request.user.username
    chats = Chat.objects.filter(user=request.user).order_by("datetime")
    items = Table.objects.all().order_by("date", "start_time")
    context = {'chats':chats, 'items':items, 'logedin': logedin, "username":username}
    return render(request, "base.html", context)

@login_required(login_url='login')
def input(request):
    user = request.user
    user_input = request.POST["input"]
    ai_output = agent(user_input, user)
    chat = Chat(user_text=user_input, ai_text=ai_output, user=request.user)
    chat.save()
    return redirect("home")

def login_page(request):
    global msg
    logedin = False
    chats = Chat.objects.filter(user__username="Guest").order_by("datetime")
    items = Table.objects.all().order_by("date", "start_time")
    context = {'chats':chats, 'items':items, 'logedin': logedin,"msg": msg}
    return render(request, "base.html", context)

@require_http_methods(["POST"])
def guest_login(request):
    user=authenticate(request,username="Guest",password="Guest@2024")
    if user is not None:
        login(request, user)
        return redirect('home')
    else:
        global msg
        msg = "Something went wrong ⚠"
        return redirect("login")

@require_http_methods(["POST"])
def user_login(request):
    username=request.POST['username']
    password=request.POST['password']
    user=authenticate(request,username=username,password=password)
    if user is not None:
        login(request, user)
        return redirect('home')
    else:
        global msg
        msg = "Username or Password is incorrect 🚫"
        return redirect("login")

def user_regiser(request):
    username=request.POST['username']
    email=request.POST['email']
    password=request.POST['password']
    global msg
    try:
        user=User.objects.create_user(username, email, password)
        user.save()
        msg = "Registration successful ✅"
        return redirect("login")
    except:
        msg = "Username already taken 🚫"
        return redirect("login")
        
def user_logout(request):
    logout(request)
    return redirect('home')