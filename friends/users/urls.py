from django.contrib import admin
from django.urls import path, include, re_path
from users.views import *


urlpatterns = [
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
    path('users/<int:pk>/append', FriendAppend.as_view())
]
