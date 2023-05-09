from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


class MyUser(AbstractUser):
    friends = models.ManyToManyField('MyUser', blank=True)


class FriendRequest(models.Model):
    sender = models.ForeignKey(MyUser, related_name="sender", on_delete=models.CASCADE)
    recipient = models.ForeignKey(MyUser, related_name="recipient", on_delete=models.CASCADE)
