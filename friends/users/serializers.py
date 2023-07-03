from django.db.models import Q
from rest_framework import serializers
from users.models import MyUser, FriendRequest, Friends


class MyUserSerializer(serializers.ModelSerializer):
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

    def create(self, validated_data):
        return FriendRequest.objects.get_or_create(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ("id", "username")

