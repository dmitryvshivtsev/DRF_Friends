from django.shortcuts import render
from rest_framework import generics
from users.serializers import UserSerializer


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
