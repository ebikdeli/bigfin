from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .models import Ticketing, Answer, FileUpload
from .serializers import TicketingSerializer, AnswerSerializer, FileUploadSerializer


class TicketingViewset(ModelViewSet):
    """Viewset for Ticketing model"""
    serializer_class = TicketingSerializer
    queryset = Ticketing.objects.all()


class AnswerViewset(ModelViewSet):
    """Viewset for Answer model"""
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()


class FileUploadViewset(ModelViewSet):
    """Viewset for FileUpload model"""
    serializer_class = FileUploadSerializer
    queryset = FileUpload.objects.all()
