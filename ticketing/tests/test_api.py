from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework import status

from ticketing.models import Ticketing, Answer, FileUpload
from ticketing.serializers import TicketingSerializer, AnswerSerializer, FileUploadSerializer


class TestTicketing(TestCase):
    def setUp(self) -> None:
        # Setup user and client then authenticate the client and create a request object and create a ticket
        user_data = {'username': 'ehsan', 'password': '123456', 'name': 'essi'}
        self.user = get_user_model().objects.create_superuser(**user_data)
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.request = APIRequestFactory().get(reverse('admin:index'))
        ticket_data = {'user': self.user, 'message': 'This is a ticket message', 'title': 'title ticket here'}
        self.ticket = Ticketing.objects.create(**ticket_data)
    
    def test_ticketing_list_api(self):
        """Test if ticketing list could be reached"""
        # Create another ticketing to get better result
        Ticketing.objects.create(user=self.user, message='Ticket_2 running', title='Ticket 2 title', emergency='2')
        # Get all ticketing using api
        response = self.client.get(reverse('ticketing:ticketing-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Get all ticketing data using serializer
        serializer = TicketingSerializer(instance=Ticketing.objects.all(), many=True, context={'request': self.request})
