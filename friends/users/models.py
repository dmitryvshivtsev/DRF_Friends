from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user.username


class FriendRequest(models.Model):
    STATUS_PENDING = 'in_process'
    STATUS_ACCEPTED = 'accepted'
    STATUS_REJECTED = 'denied'
    STATUS_CHOICES = (
        (STATUS_PENDING, 'In_process'),
        (STATUS_ACCEPTED, 'Accepted'),
        (STATUS_REJECTED, 'Denied'),
    )

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requests_sent')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requests_received')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)

    def accept(self):
        self.status = self.STATUS_ACCEPTED
        self.save()

        reciprocal_request = FriendRequest(sender=self.recipient, recipient=self.sender, status=self.STATUS_ACCEPTED)
        reciprocal_request.save()

    def reject(self):
        self.status = self.STATUS_REJECTED
        self.save()

    class Meta:
        unique_together = ('sender', 'recipient')

