from django.contrib import admin
from django.urls import path, include, re_path
from users.views import *


urlpatterns = [
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
    path('friends/requests/', FriendRequestList.as_view()),
    path('friends/requests/<int:request_id>/accept/', AcceptFriendRequest.as_view()),
    path('friends/requests/<int:request_id>/denied/', RejectFriendRequest.as_view()),
    path('friends/send-request/<int:pk>/', SendFriendRequest.as_view()),
]
