from django.contrib import admin
from django.urls import path, include, re_path
from users.views import *


app_name = 'friends'
urlpatterns = [
    path('user/create/', UserCreateView.as_view())
]