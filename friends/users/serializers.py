from users.models import MyUser, FriendRequest
from rest_framework import serializers


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ('id', 'sender', 'recipient', 'status', )
        read_only_fields = ('id', )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'user', 'friends']

#
# class FriendRequestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FriendRequest
#         fields = ['sender_id', 'recipient_id', 'status']
