"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse

from .views import main_spa, login_view, signup_view, auth_status,logout_view,change_user_password,get_csrf_token



urlpatterns = [
    path('', main_spa, name='home'),
    path('login/', login_view, name='login'), 
    path('signup/', signup_view, name='signup'), 
    path('auth-status/', auth_status, name='auth_status'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/change-password/', change_user_password, name='change_user_password'),
    path('csrf/', get_csrf_token, name='get_csrf_token'),
]
