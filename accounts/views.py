from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework import permissions
from rest_framework import authentication
from django_filters import rest_framework as filters

from .models import Address
from .serializers import UserSerializer, AddressSerializer
from .filters import UserFilterSet, AddressFilterSet


class UserViewSet(ModelViewSet):
    """This ViewSet used for list, retreive, post and update User model"""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser, ]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = UserFilterSet
    

class AddressViewSet(ModelViewSet):
    """This ViewSet used for list, retreive, post and update Address model"""
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAdminUser, ]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = AddressFilterSet
