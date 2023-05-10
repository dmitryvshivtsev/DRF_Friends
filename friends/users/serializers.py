from rest_framework import serializers
from users.models import MyUser, FriendRequest


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'username')


class FriendListSerializer(serializers.ModelSerializer):
    friends = MyUserSerializer(many=True)

    class Meta:
        model = MyUser
        fields = ('id', 'username', 'friends')


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ('id', 'sender', 'recipient')


class SendRequestSerializer(serializers.Serializer):
    recipient_id = serializers.IntegerField()

    def create(self, validated_data):
        sender = self.context['request'].user
        recipient = MyUser.objects.get(id=validated_data['recipient_id'])
        frequest = FriendRequest.objects.get_or_create(sender=sender, recipient=recipient)
        return frequest


class FriendStatusSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = MyUser
        fields = ('id', 'username', 'status')

    def get_status(self, profile_user):
        user = self.context['request'].user
        if user == profile_user:
            return "Это ваша страница"
        elif user.sender.filter(recipient=profile_user).exists() \
                and user.recipient.filter(sender=profile_user).exists():
            return "Уже друзья"
        elif user.sender.filter(recipient=profile_user).exists():
            return "Исходящая заявка"
        elif user.recipient.filter(sender=profile_user).exists():
            return "Входящая заявка"
        else:
            return "Нет ничего"

