from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from users.serializers import *
from users.models import MyUser, FriendRequest, Friends
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
        user_id = MyUser.objects.get(id=request.user.id).id
        print(user_id)
        friends = MyUser.objects.filter(Q(user_id_1__user_id_2=user_id) | Q(user_id_2__user_id_1=user_id))
        all_friends = MyUserSerializer(friends, many=True)
        data = {
            'all_friends': all_friends.data
        }
        return Response(data, status=status.HTTP_200_OK)


class IncomingRequestsView(APIView):
    """ Просмотреть входящие заявки """

    def get(self, request):
        incoming = FriendRequest.objects.filter(recipient=request.user.id)
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

    def post(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        data = {
            'recipient_id': pk
        }
        context = {
            'sender_name': request.user
        }
        serializer = SendRequestSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class AcceptFriendRequestView(APIView):
    """ Принять заявку в друзья """

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


class RejectFriendRequestView(APIView):
    """ Отменить отправленную заявку """

    def delete(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        friend_request = FriendRequest.objects.filter(sender_id=pk).first()
        if friend_request:
            # удаляем записи из базы
            friend_request.delete()
            FriendRequest.objects.filter(recipient_id=pk).first().delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class RemoveFriendView(APIView):
    """ Удалить юзера из друзей """

    def delete(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        user_id_1 = MyUser.objects.get(id=request.user.id).id
        user_id_2 = pk
        remove_entry = Friends.objects.filter(
            (
                    Q(user_id_1=user_id_1) | Q(user_id_1=user_id_2)
            ) & (
                    Q(user_id_2=user_id_1) | Q(user_id_2=user_id_2)
            )
        )
        remove_entry.delete()
        return Response(status=status.HTTP_200_OK)


class FriendStatusView(generics.RetrieveAPIView):
    """ Получить статус дружбы """
    queryset = MyUser.objects.all()
    serializer_class = FriendStatusSerializer
    lookup_field = 'pk'  # получаем инфо по id объекта

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context
