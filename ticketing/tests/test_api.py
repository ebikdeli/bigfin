from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from ticketing.models import Ticketing, Answer, FileUpload
from ticketing.serializers import TicketingSerializer, AnswerSerializer, FileUploadSerializer
