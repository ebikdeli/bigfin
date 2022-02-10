"""
https://www.django-rest-framework.org/api-guide/serializers/#including-extra-context
"""
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework import authentication
from rest_framework import status
from rest_framework.response import Response
from django_filters import rest_framework as filters

from .models import Ticketing, Answer, FileUpload
from .serializers import TicketingSerializer, AnswerSerializer, FileUploadSerializer
from .filters import TicketingFilterSet, AnswerFilterSet, FileUploadFilterSet


class TicketingViewset(ModelViewSet):
    """Viewset for Ticketing model"""
    serializer_class = TicketingSerializer
    queryset = Ticketing.objects.all()
    permission_classes = [permissions.IsAdminUser, ]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = TicketingFilterSet

    def list(self, request, *args, **kwargs):
        """Override 'list' method to send 'request' object to serializer - although it's not needed for ModelSerializer"""
        queryset = Ticketing.objects.all()
        serializer = TicketingSerializer(instance=queryset, many=True, context={'request': request, 'name': 'ehsan'})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class AnswerViewset(ModelViewSet):
    """Viewset for Answer model"""
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
    permission_classes = [permissions.IsAdminUser, ]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = AnswerFilterSet

    def list(self, request, *args, **kwargs):
        """Override 'list' method to send 'request' object to serializer - although it's not needed for ModelSerializer"""
        queryset = Answer.objects.all()
        serializer = AnswerSerializer(instance=queryset, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class FileUploadViewset(ModelViewSet):
    """Viewset for FileUpload model"""
    serializer_class = FileUploadSerializer
    queryset = FileUpload.objects.all()
    permission_classes = [permissions.IsAdminUser, ]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = FileUploadFilterSet

    def list(self, request, *args, **kwargs):
        """Override 'list' method to send 'request' object to serializer - although it's not needed for ModelSerializer"""
        queryset = FileUpload.objects.all()
        serializer = FileUploadSerializer(instance=queryset, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)
