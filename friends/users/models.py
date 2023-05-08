from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    friends = ArrayField(models.IntegerField(), blank=True, null=True)


class FriendRequest(models.Model):
    sender = models.ForeignKey(User, related_name='sent', verbose_name='Отправитель', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='incoming', verbose_name='Получатель', on_delete=models.CASCADE)
    STATUS = (
        (1, 'in_process'),
        (2, 'ok'),
        (3, 'denied'),
    )
    status = models.IntegerField(verbose_name='Статус', choices=STATUS)

