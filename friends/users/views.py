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
    serializer_class = MyUserSerializer


class UserFriendsView(APIView):
    """Список друзей"""

    def get(self, request):
        user_id = MyUser.objects.get(id=request.user.id).id
        friends = MyUser.objects.filter(
            Q(user_id_1__user_id_2=user_id) | Q(user_id_2__user_id_1=user_id)
        )
        all_friends = MyUserSerializer(friends, many=True)
        data = {"all_friends": all_friends.data}
        return Response(data, status=status.HTTP_200_OK)


class IncomingRequestsView(APIView):
    """Просмотреть входящие заявки"""

    def get(self, request):
        incoming = FriendRequest.objects.filter(recipient=request.user.id)
        incoming_serializer = FriendRequestSerializer(incoming, many=True)
        data = {"incoming": incoming_serializer.data}
        return Response(data, status=status.HTTP_200_OK)


class OutcomingRequestsView(APIView):
    """Просмотреть исходящие заявки"""

    def get(self, request):
        outcoming = FriendRequest.objects.filter(sender=request.user)
        outcoming_serializer = FriendRequestSerializer(outcoming, many=True)
        data = {"outcoming": outcoming_serializer.data}
        return Response(data, status=status.HTTP_200_OK)


class SendFriendRequestView(APIView):
    """Отправить заявку в друзья"""

    def post(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        data = {"sender_id": request.user.id, "recipient_id": pk}
        serializer = FriendRequestSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class AcceptFriendRequestView(APIView):
    """Принять заявку в друзья"""

    def post(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        friend_request = FriendRequest.objects.filter(sender_id=pk).first()
        if friend_request:
            # create new entry in the Friends database
            sender = friend_request.sender
            recipient = friend_request.recipient
            Friends.objects.create(user_id_1=sender, user_id_2=recipient)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CancelFriendRequestView(APIView):
    """Отменить отправленную заявку"""

    def delete(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        recipient = pk
        sender = MyUser.objects.get(id=request.user.id).id
        remove_entry = FriendRequest.objects.filter(
            Q(sender_id=sender) & Q(recipient_id=recipient)
        )
        remove_entry.delete()
        return Response(status=status.HTTP_200_OK)


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
        pk = kwargs["pk"]
        user_friends = MyUser.objects.filter(
            Q(user_id_1__user_id_2=pk) | Q(user_id_2__user_id_1=pk)
        )
        user_profile = get_object_or_404(MyUser, id=pk).username
        user_friends_serializer = UserProfileSerializer(user_friends, many=True)
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
