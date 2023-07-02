from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


class MyUser(AbstractUser):
    """Расширение стандартной модели пользователя"""

    friends = models.ManyToManyField("MyUser", blank=True)


class FriendRequest(models.Model):
    """Модель хранящая заявки от пользователей"""

    sender = models.ForeignKey(MyUser, related_name="sender", on_delete=models.CASCADE)
    recipient = models.ForeignKey(
        MyUser, related_name="recipient", on_delete=models.CASCADE
    )


class Friends(models.Model):
    """Модель хранящая информацию о друзьях"""

    user_id_1 = models.ForeignKey(
        MyUser, related_name="user_id_1", on_delete=models.CASCADE
    )
    user_id_2 = models.ForeignKey(
        MyUser, related_name="user_id_2", on_delete=models.CASCADE
    )
