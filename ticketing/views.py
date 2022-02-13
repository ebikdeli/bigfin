"""
https://www.django-rest-framework.org/api-guide/serializers/#including-extra-context

In this module we can do diffrent things based on diffrent 'actions'. We can even define our own
actions in DRF. More information found in the following documents:
https://www.django-rest-framework.org/api-guide/viewsets/#viewset-actions
https://www.django-rest-framework.org/api-guide/viewsets/#introspecting-viewset-actions

To filter the data returned by 'list' action, we can use 'query_params' attributes on DRF Views in 'request' object.
Acctually This document explains it better:
https://www.django-rest-framework.org/api-guide/requests/#query_params

To see what attributes and methods could be used and overrided in APIViews, Generic Views and Viewsets, see
documents below:
https://www.django-rest-framework.org/api-guide/views/#api-policy-attributes
https://www.django-rest-framework.org/api-guide/generic-views/#genericapiview

"""
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework import authentication
from rest_framework import status
from rest_framework.response import Response
# from rest_framework.request import Request
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
    # queryset = Answer.objects.all()
    # permission_classes = [permissions.IsAdminUser, ]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = AnswerFilterSet

    def get_queryset(self):
        """override get_queryset method."""
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                queryset = Answer.objects.all()
            else:
                queryset = Answer.objects.filter(user=self.request.user)
        else:
            queryset = Answer.objects.none()
        return queryset

    def list(self, request, *args, **kwargs):
        """Override 'list' method to send 'request' object to serializer - although it's not needed for ModelSerializer"""
        # Per DRF documents it's so much faster to use 'get_queryset' method rather than 'queryset' attribute
        # queryset = Answer.objects.all()
        queryset = self.get_queryset()
        print('query_params: ', self.request.query_params)
        if queryset.exists():
            serializer = AnswerSerializer(instance=queryset, many=True, context={'request': request})
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data='Error: This user is not authenticated!', status=status.HTTP_200_OK)


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
