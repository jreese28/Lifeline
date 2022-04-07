"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from django.contrib import admin
from . import views
from django.urls import path, re_path
from .views import HomePageView, AddPageView, ProfilePageView, LogInPageView, LoggedInPageView
from main.views import postSignIn

app_name = "main"

urlpatterns = [
    #path("loggedin/", LoggedInPageView.as_view(), name="loggedin"),
    re_path(r'^loggedin/$',postSignIn, name="loggedin"),
    path("login/", LogInPageView.as_view(), name="login"),
    path("profile/", ProfilePageView.as_view(), name="profile"),
    path("add/", AddPageView.as_view(), name="add"),
    #path("", HomePageView.as_view(), name="home"),
    #path("", views.index, name ="homepage"),

    path("", views.index, name ="homepage"),
    #path("/add.html", views.add, name ="add"),
]
