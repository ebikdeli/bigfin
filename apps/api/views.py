from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer


class UserListView(ListAPIView):
    """Generic view for User list"""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]

    def list(self, request, *args, **kwargs):
        # This is only shows how 'authentication token' shown in DRF views
        print(request.user)
        print(request.auth)
        serializer = UserSerializer(get_user_model().objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
