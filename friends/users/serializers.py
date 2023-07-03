from django.db.models import Q
from rest_framework import serializers
from users.models import MyUser, FriendRequest, Friends


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ("id", "username")


# class FriendRequestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FriendRequest
#         fields = ("id", "sender", "recipient")
#

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


class FriendStatusSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = MyUser
        fields = ("id", "username", "status")

    def get_status(self, user_profile):
        own_user = self.context["request"].user
        if own_user == user_profile:
            return "Это ваша страница"
        elif (
            Friends.objects.filter(
                    (Q(user_id_1=own_user.id) | Q(user_id_1=user_profile.id))
                    & (Q(user_id_2=own_user.id) | Q(user_id_2=user_profile.id))
            ).exists()
        ):
            return "Уже друзья"
        elif own_user.sender.filter(recipient=user_profile).exists():
            return "Исходящая заявка"
        elif own_user.recipient.filter(sender=user_profile).exists():
            return "Входящая заявка"
        else:
            return "Нет ничего"
