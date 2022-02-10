"""
** It's highly recommended to override 'viewset' list or retreive method to send 'request' via the Serializer
'context' attribute to be able do somethings in Serializer body.

** When we use Serailizer inheritance, we can use in serializer class we want among parent or child
class.
"""
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework import permissions
from rest_framework import authentication
from rest_framework.response import Response
from django_filters import rest_framework as filters

from .models import Address
from .serializers import UserSerializer, AddressSerializer, UserNewSerializer
from .filters import UserFilterSet, AddressFilterSet


class UserViewSet(ModelViewSet):
    """This ViewSet used for list, retreive, post and update User model"""
    queryset = get_user_model().objects.all()
    serializer_class = UserNewSerializer
    permission_classes = [permissions.IsAdminUser, ]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = UserFilterSet

    def list(self, request, *args, **kwargs):
        """Override 'list' method to send 'request' object to serializer - although it's not needed for ModelSerializer"""
        queryset = get_user_model().objects.all()
        serializer = UserNewSerializer(instance=queryset, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    

class AddressViewSet(ModelViewSet):
    """This ViewSet used for list, retreive, post and update Address model"""
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAdminUser, ]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = AddressFilterSet

    def list(self, request, *args, **kwargs):
        """Override 'list' method to send 'request' object to serializer - although it's not needed for ModelSerializer"""
        queryset = Address.objects.all()
        serializer = AddressSerializer(instance=queryset, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)
