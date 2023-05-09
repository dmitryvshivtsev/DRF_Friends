from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializers import *
from users.models import MyUser, FriendRequest
from django.db.models import Q


class AllUsersView(APIView):
    """ Список всех зарегестрированных пользователей """
    def get(self, request):
        all_users = MyUser.objects.exclude(username=request.user)
        all_users_serializer = MyUserSerializer(all_users, many=True)
        data = {
            'all_users': all_users_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)


class UserFriendsView(APIView):
    """ Список друзей """
    def get(self, request):
        user = MyUser.objects.get(id=request.user.id)
        friends = MyUser.objects.filter(Q(sender__recipient=user, recipient__sender=user)).distinct()
        all_friends = MyUserSerializer(friends, many=True)
        data = {
            'all_friends': all_friends.data
        }
        return Response(data, status=status.HTTP_200_OK)


class IncomingRequestsView(APIView):
    """ Просмотреть входящие заявки """
    def get(self, request):
        incoming = FriendRequest.objects.filter(recipient=request.user)
        incoming_serializer = FriendRequestSerializer(incoming, many=True)
        data = {
            'incoming': incoming_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)


class OutcomingRequestsView(APIView):
    """ Просмотреть исходящие заявки """
    def get(self, request):
        outcoming = FriendRequest.objects.filter(sender=request.user)
        outcoming_serializer = FriendRequestSerializer(outcoming, many=True)
        data = {
            'outcoming': outcoming_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)


class SendFriendRequestView(APIView):
    """ Отправить заявку в друзья """
    serializer_class = SendRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class AcceptFriendRequestView(APIView):
    """ Принять заявку в друзья """
    def post(self, request, id):
        friend_request = FriendRequest.objects.filter(sender_id=id).first()
        if friend_request:
            sender = friend_request.sender
            recipient = friend_request.recipient
            FriendRequest.objects.create(sender=recipient, recipient=sender)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class RejectFriendRequestView(APIView):
    """ Удалить из друзей или отклонить заявку """
    def post(self, request, id):
        friend_request = FriendRequest.objects.filter(sender_id=id).first()
        if friend_request:
            friend_request.delete()
            FriendRequest.objects.filter(recipient_id=id).first().delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

