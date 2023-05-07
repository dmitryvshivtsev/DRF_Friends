from django.contrib import admin
from users.models import MyUser, FriendRequest

# Register your models here.
admin.register(MyUser, FriendRequest)