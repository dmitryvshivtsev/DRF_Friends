from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from users.serializers import *
from users.models import MyUser, FriendRequest, Friends
from django.db.models import Q


class AllUsersView(generics.ListAPIView):
    """Список всех зарегестрированных пользователей"""
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer


class UserFriendsView(generics.ListAPIView):
    """Список друзей"""
    serializer_class = UserSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        friends = MyUser.objects.filter(
            Q(user_id_1__user_id_2=user_id) | Q(user_id_2__user_id_1=user_id)
        )
        return friends


class IncomingRequestsView(generics.ListAPIView):
    """Просмотреть входящие заявки"""
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        incoming = FriendRequest.objects.filter(recipient=self.request.user.id)
        return incoming


class OutcomingRequestsView(generics.ListAPIView):
    """Просмотреть исходящие заявки"""
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        outcoming = FriendRequest.objects.filter(sender=self.request.user.id)
        return outcoming


class SendFriendRequestView(generics.CreateAPIView):
    """Отправить заявку в друзья"""

    serializer_class = FriendRequestSerializer

    def perform_create(self, serializer):
        serializer.save(sender_id=self.request.user.id, recipient_id=self.kwargs["pk"])


class AcceptFriendRequestView(generics.CreateAPIView):
    """Принять заявку в друзья"""

    serializer_class = FriendsSerializer

    def perform_create(self, serializer):
        friend_request = FriendRequest.objects.filter(sender_id=self.kwargs["pk"]).first()
        serializer.save(user_id_1=friend_request.sender, user_id_2=friend_request.recipient)
        friend_request.delete()


class CancelFriendRequestView(generics.RetrieveDestroyAPIView):
    """Отменить отправленную заявку"""

    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer

    def perform_destroy(self, instance):
        sender = self.request.user.id
        recipient = instance.recipient_id
        remove_entry = FriendRequest.objects.filter(
            sender_id=sender, recipient_id=recipient
        )
        remove_entry.delete()


class RemoveFriendView(APIView):
    """Удалить юзера из друзей"""

    def delete(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        sender = MyUser.objects.get(id=request.user.id).id
        recipient = pk
        remove_entry = Friends.objects.filter(
            (Q(user_id_1=sender) | Q(user_id_1=recipient))
            & (Q(user_id_2=sender) | Q(user_id_2=recipient))
        )
        remove_entry.delete()
        data = {"sender_id": recipient, "recipient_id": sender}
        serializer = FriendRequestSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class UserProfileView(APIView):
    """Профиль пользователя"""

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        user_friends = MyUser.objects.filter(
            Q(user_id_1__user_id_2=pk) | Q(user_id_2__user_id_1=pk)
        )
        user_profile = get_object_or_404(MyUser, id=pk).username
        user_friends_serializer = UserSerializer(user_friends, many=True)
        own_user = self.request.user
        friend_status = "Ничего"
        if user_profile == str(own_user):
            friend_status = "Это ваша страница :)"
        elif (
            Friends.objects.filter(
                    (Q(user_id_1=own_user.id) | Q(user_id_1=pk))
                    & (Q(user_id_2=own_user.id) | Q(user_id_2=pk))
            ).exists()
        ):
            friend_status = "Уже друзья"
        elif own_user.sender.filter(recipient=pk).exists():
            friend_status = "Исходящая заявка"
        elif own_user.recipient.filter(sender=pk).exists():
            friend_status = "Входящая заявка"
        data = {
            "id": pk,
            "user_profile": user_profile,
            "friend_status": friend_status,
            "user_friends": user_friends_serializer.data
        }
        return Response(data=data, status=status.HTTP_200_OK)
