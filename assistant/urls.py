from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('input', views.input, name="input"),
    path('login-page', views.login_page, name="login"),
    path('guest', views.guest_login),
    path('login', views.user_login),
    path('register', views.user_regiser),
    path('logout', views.user_logout),
]