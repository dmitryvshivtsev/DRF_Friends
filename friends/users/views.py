from rest_framework.views import APIView
from rest_framework import generics
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
        user_id = MyUser.objects.get(id=request.user.id).id
        friends = MyUser.objects.filter(Q(user_id_1=user_id) | Q(user_id_2=user_id))
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

    serializer_class = SendRequestSerializer

    def post(self, request, id):
        # отправляем заявку в друзья
        serializer = self.serializer_class(data={"recipient_id": id}, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class AcceptFriendRequestView(APIView):
    """ Принять заявку в друзья """

    def post(self, request, id):
        friend_request = FriendRequest.objects.filter(sender_id=id).first()
        if friend_request:
            # добавляем в базу взаимную заявку, если принимаем запрос
            sender = friend_request.sender
            recipient = friend_request.recipient
            FriendRequest.objects.get_or_create(sender=recipient, recipient=sender)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class RejectFriendRequestView(APIView):
    """ Отклонить заявку """

    def post(self, request, id):
        friend_request = FriendRequest.objects.filter(sender_id=id).first()
        if friend_request:
            # удаляем записи из базы
            friend_request.delete()
            FriendRequest.objects.filter(recipient_id=id).first().delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        pass


class RemoveFriendView(APIView):
    pass


class FriendStatusView(generics.RetrieveAPIView):
    """ Получить статус дружбы """
    queryset = MyUser.objects.all()
    serializer_class = FriendStatusSerializer
    lookup_field = 'id'  # получаем инфо по id объекта

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context
