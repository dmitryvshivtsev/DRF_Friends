from django.db.models import Q
from rest_framework import serializers
from users.models import MyUser, FriendRequest, Friends


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ("id", "username")


class FriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friends
        fields = ("id", "user_id_1", "user_id_2")


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ("sender", "recipient")


