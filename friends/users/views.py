from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from users.models import User, MyUser, FriendRequest
from users.serializers import UserSerializer, FriendRequestSerializer
from users.queries import get_user_friends
from rest_framework import permissions
from django.db.models import Q


class SendFriendRequest(generics.CreateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer

    def post(self, request, *args, **kwargs):
        recipient = kwargs.get('pk')
        if request.user.id == recipient:
            return Response({'error': 'You cannot send friend request to yourself'}, status=status.HTTP_400_BAD_REQUEST)
        if FriendRequest.objects.filter(sender=request.user, recipient_id=recipient).exists():
            return Response({'error': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)
        friend_request = FriendRequest(sender=request.user, recipient_id=recipient)
        friend_request.save()
        serializer = FriendRequestSerializer(friend_request)
        return Response(serializer.data)


class FriendRequestList(generics.ListAPIView):
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return FriendRequest.objects.filter(recipient_id=user_id, status=FriendRequest.STATUS_PENDING)

    def post(self, request, *args, **kwargs):
        friend_request_id = request.data.get('friend_request_id')
        action = request.data.get('action')
        if action == 'accept':
            friend_request = FriendRequest.objects.get(id=friend_request_id, recipient=request.user)
            friend_request.accept()
            serializer = FriendRequestSerializer(friend_request)
            return Response(serializer.data)
        elif action == 'denied':
            friend_request = FriendRequest.objects.get(id=friend_request_id, recipient=request.user)
            friend_request.reject()
            serializer = FriendRequestSerializer(friend_request)
            return Response(serializer.data)
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)


class AcceptFriendRequest(APIView):
    def post(self, request, request_id):
        friend_request = FriendRequest.objects.get(id=request_id)
        friend_request.status = 'accepted'
        friend_request.save()
        return Response(status=status.HTTP_200_OK)


class RejectFriendRequest(APIView):
    def post(self, request, request_id):
        friend_request = FriendRequest.objects.get(id=request_id)
        friend_request.status = 'denied'
        friend_request.save()
        return Response(status=status.HTTP_200_OK)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FriendAppend(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = permissions.IsAuthenticated

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
