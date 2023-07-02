from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    def __str__(self):
        return f"{self.username} | {self.first_name}"
