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

from .views import *


"""
This defines the url patterns for the project ,and will map the routes to their corresponding views
"""
urlpatterns = [
    path('', main_spa, name='home'),
    path('login/', login_view, name='login'), 
    path('signup/', signup_view, name='signup'), 
    path('auth-status/', auth_status, name='auth_status'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/change-password/', change_user_password, name='change_user_password'),
    path('csrf/', get_csrf_token, name='get_csrf_token'),
    path('profile/create-hobby/', create_new_hobby, name='create_new_hobby'),
    path('profile/update/', update_profile, name='update_profile'),
    path('hobbies/', get_all_hobbies, name='get_all_hobbies'),
    path('profile/add-hobby/', add_hobby, name='add_hobby'),
    path('check-user-hobby/', check_user_hobby, name='check_user_hobby'),
    path('profile/remove-hobby/', remove_hobby, name='remove_hobby'),
    path('users/', get_users, name='get_users'),
    path('users/similar-hobbies/', get_users_with_similar_hobbies, name='get_users_with_similar_hobbies'),
    path('send-friend-request/', send_friend_request, name='send_friend_request'),
    path('friend-requests/', list_friend_requests, name='list_friend_requests'),
    path('remove-friend-request/', remove_friend_request, name='remove_friend_request'),
    path('accept-friend-request/', accept_friend_request, name='accept_friend_request'),
    path('api/friends/', show_friends, name='show_friends'),
    
]
