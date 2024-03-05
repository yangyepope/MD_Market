from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, GenericAPIView

from .serializers import UserSerializer


# Create your views here.


class UserView(CreateAPIView):
    """用户注册"""
    serializer_class = UserSerializer

    # def post(self, request, *args, **kwargs):
    #     print(self.request.data)
