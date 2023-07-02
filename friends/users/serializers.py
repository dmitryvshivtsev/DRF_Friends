from rest_framework import serializers
from users.models import MyUser, FriendRequest, Friends


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ("id", "username")


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ("id", "sender", "recipient")


class FriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friends
        fields = ("id", "user_id_1", "user_id_2")


class SendRequestSerializer(serializers.Serializer):
    recipient_id = serializers.IntegerField()

    def create(self, validated_data):
        sender = self.context["sender_name"]  # get id of user who send request
        recipient = MyUser.objects.get(id=self.data["recipient_id"])
        return FriendRequest.objects.get_or_create(sender=sender, recipient=recipient)


class FriendStatusSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = MyUser
        fields = ("id", "username", "status")

    def get_status(self, profile_user):
        user = self.context["request"].user
        if user == profile_user:
            return "Это ваша страница"
        elif (
            user.sender.filter(recipient=profile_user).exists()
            and user.recipient.filter(sender=profile_user).exists()
        ):
            return "Уже друзья"
        elif user.sender.filter(recipient=profile_user).exists():
            return "Исходящая заявка"
        elif user.recipient.filter(sender=profile_user).exists():
            return "Входящая заявка"
        else:
            return "Нет ничего"
