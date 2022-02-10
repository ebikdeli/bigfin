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
        self.assertIsNotNone(serializer.data)
        
        self.assertEqual(serializer.data, response.json())
    
    def test_ticketing_reterive_api(self):
        """Test if we can retreive a ticket successfully"""
        # Retreive a ticket
        # Remember that the 'kwargs' arguement in 'reverse' function only accepts two keys: "pk" or "slug".
        # Even if we put 'id' instead of "PK" we will get error.
        response = self.client.get(reverse('ticketing:ticketing-detail', kwargs={'pk': self.ticket.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Retreive same ticket using serializer
        serializer = TicketingSerializer(instance=self.ticket, many=False, context={'request': self.request})
        self.assertIsNotNone(serializer.data)

        self.assertEqual(response.json(), serializer.data)

    def test_ticketing_create_bad_data_api(self):
        """Test if ticket error for bad data when creating a ticket"""
        # 'user' is 'read_only' field and couldn't be used to create or update Ticket object
        bad_data = {'user': self.user, 'message': 'Hello', 'title': 'Title'}
        response = self.client.post(path=reverse('ticketing:ticketing-list'), data=bad_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_ticketing_create_api(self):
        """Test if we can create a ticket using api"""
        # Remember that when using api, we should use 'lookup_field' as ForeignKey field or ManyToMany Field or
        # 'related_name' field to send needed object to serializer unlike the regular django that could take an
        # object directly to create or update or get an object. By default 'lookup_field' is Model's 'pk' or 'id'
        # field but we can change it in Views and serializers - REMEMBER TO SET A UNIQUE=TRUE FIELD AS looku_field.

        # Create ticket using 'user_obj' field:
        ticket_data_user_obj = {'user_obj': self.user.id, 'title': 'This is title', 'message': 'This is message'}
        response_user_obj = self.client.post(reverse('ticketing:ticketing-list'), data=ticket_data_user_obj)
        self.assertEqual(response_user_obj.status_code, status.HTTP_201_CREATED)

        # Create ticket using 'username' field:
        ticket_data_username = {'username': self.user.username, 'title': 'This is title', 'message': 'This is message'}
        response_username = self.client.post(reverse('ticketing:ticketing-list'), data=ticket_data_username)
        self.assertEqual(response_username.status_code, status.HTTP_201_CREATED)

        # Createing using both 'user_obj' and 'username' field:
        ticket_data_both = {'username': self.user.username,
                            'user_obj': self.user.id,
                            'title': 'This is title',
                            'message': 'This is message'}
        response_both = self.client.post(reverse('ticketing:ticketing-list'), data=ticket_data_both)
        self.assertEqual(response_both.status_code, status.HTTP_201_CREATED)
    
    def test_ticketing_delete_api(self):
        """Test if we can delete ticketing using api"""
        # Test if ticket exist:
        self.assertIsNotNone(Ticketing.objects.filter(ticket_id=self.ticket.ticket_id).first())

        # Delete ticket
        response = self.client.delete(reverse('ticketing:ticketing-detail', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Test if ticket not exist
        self.assertIsNone(Ticketing.objects.filter(ticket_id=self.ticket.ticket_id).last())
    
    def test_ticketing_partial_update_api(self):
        """Test if partial update of ticket is successful (patch method)"""
        old_title = self.ticket.title
        old_message = self.ticket.message
        data = {'username': self.user.username, 'title': 'New title'}
        response = self.client.patch(path=reverse('ticketing:ticketing-detail', kwargs={'pk': self.ticket.id}), data=data)

        # Update object in the database
        self.ticket.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(self.ticket.title, old_title)
        self.assertEqual(self.ticket.message, old_message)
    
    def test_ticketing_total_update_api(self):
        """Test if total update of ticket is successful (put method)"""
        old_title = self.ticket.title
        old_message = self.ticket.message
        # Because 'put' method replaces all fields in the serializer, we need to set all required fields for seializer
        bad_data = {'user_obj': self.user.id, 'title': 'New title'}
        bad_response = self.client.put(path=reverse('ticketing:ticketing-detail', kwargs={'pk': self.ticket.id}), data=bad_data)
        self.assertEqual(bad_response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {'user_obj': self.user.id, 'title': 'New title', 'message': 'New message'}
        response = self.client.put(path=reverse('ticketing:ticketing-detail', kwargs={'pk': self.ticket.id}), data=data)

        # Update object in the database
        self.ticket.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(self.ticket.title, old_title)
        self.assertNotEqual(self.ticket.message, old_message)
    

class TestAnswer(TestCase):
    def setUp(self) -> None:
        # Create a super user
        user_data = {'username': 'ehsan', 'password': '123456', 'name': 'essi'}
        self.user = get_user_model().objects.create_superuser(**user_data)

        # Create a clinet and login with the user
        self.client = APIClient()
        self.client.login(**user_data)

        # Create a 'request' object
        self.request = APIRequestFactory().get('admin:index')

        # Create a Ticket
        ticket_data = {'user': self.user, 'message': 'This is Ticket message', 'title': 'This is Ticket title'}
        self.ticket = Ticketing.objects.create(**ticket_data)

        # Create a Answer
        answer_data = {'user': self.user, 'ticketing': self.ticket, 'message': 'This is Anwer message'}
        self.answer = Answer.objects.create(**answer_data)
    
    def test_answer_list_api(self):
        """Test if serializer works properly"""
        a_data_1 = {'user': self.user, 'ticketing': self.ticket, 'message': 'answer message 1'}
        a_data_2 = {'user': self.user, 'ticketing': self.ticket, 'message': 'answer message 2'}
        # https://docs.djangoproject.com/en/4.0/ref/models/querysets/#bulk-create
        answer_1, answer_2 = Answer.objects.bulk_create([Answer(**a_data_1), Answer(**a_data_2)])
        self.assertNotEqual(answer_1.message, answer_2.message)

        response = self.client.get(path=reverse('ticketing:answer-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = AnswerSerializer(instance=Answer.objects.all(), many=True, context={'request': self.request})

        self.assertEqual(response.json(), serializer.data)
    
    def test_answer_retreive_api(self):
        """Test if retreive answer properly using api"""
        response = self.client.get(reverse('ticketing:answer-detail', kwargs={'pk': self.answer.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = AnswerSerializer(instance=self.answer, many=False, context={'request': self.request})

        self.assertEqual(response.json(), serializer.data)
    
    def test_anwer_create_bad_api(self):
        """Test effect of bad request on the post method"""
        # 'post' method only accepts 'serializable data' not arbitrary objects such as 'User' and 'Ticket'
        bad_data = {'user_obj': self.user, 'ticketing_obj': self.ticket, 'message': 'Bad request'}
        response = self.client.post(reverse('ticketing:answer-list'), data=bad_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        serializer = AnswerSerializer(Answer.objects.last(), many=False, context={'request': self.request})

        self.assertNotEqual(response.json(), serializer.data)
    
    def test_answer_create_api(self):
        """Test if new answer created properly"""
        # We can get 'ticket' object for creating answer in 4 ways with 4 fields in the AnswerSerailizer:
        # 1- Using 'user_obj' and 'ticketing_obj'
        # 2- Using 'username' and 'ticketing_obj'
        # 3- Using 'user_obj' and 'ticket_id'
        # 4- Using 'username' and 'ticket_id'
        # We can use any way we want but rememeber that for 'user_obj' and 'ticketing_obj' we need to get
        # them with 'lookup_field' or in this case the field is 'id':
        answer_data_1 = {'user_obj': self.user.id, 'ticket_id': self.ticket.ticket_id, 'message': 'This is message answer'}
        response_1 = self.client.post(reverse('ticketing:answer-list'), data=answer_data_1)
        self.assertEqual(response_1.status_code, status.HTTP_201_CREATED)

        serializer = AnswerSerializer(instance=Answer.objects.last(), many=False, context={'request': self.request})

        self.assertEqual(response_1.json(), serializer.data)

        # Making another answer for fun
        answer_data_2 = {'username': self.user.username, 'ticketing_obj': self.ticket.id, 'message': 'This is message answer'}
        response_2 = self.client.post(reverse('ticketing:answer-list'), data=answer_data_2)

        self.assertEqual(response_2.status_code, status.HTTP_201_CREATED)
        
    def test_answer_partially_update_api(self):
        """Test 'patch' method to partially update an answer with api"""
        # Test current ticket title of the answer
        old_ticket_title = self.answer.ticketing.title
        self.assertEqual(self.answer.ticketing.title, old_ticket_title)

        # Create new a Ticket and update the answer with this new ticket
        new_ticket = Ticketing.objects.create(user=self.user, title='New Ticket tile')
        new_data = {'username': self.user.username, 'ticketing_obj': new_ticket.id}
        response = self.client.patch(reverse('ticketing:answer-detail', kwargs={'pk': self.answer.id}), data=new_data)

        # Refresh answer object to show new data
        self.answer.refresh_from_db()

        serializer = AnswerSerializer(instance=self.answer, many=False, context={'request': self.request})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serializer.data)
        self.assertNotEqual(self.answer.ticketing.title, old_ticket_title)
    
    def test_answer_totally_update_api(self):
        """Test 'put' method to totally update an answer with api"""
        # Test current ticket title of the answer
        old_ticket_title = self.answer.ticketing.title
        self.assertEqual(self.answer.ticketing.title, old_ticket_title)

        # Create new a Ticket and update the answer with this new ticket
        new_ticket = Ticketing.objects.create(user=self.user, title='New Ticket tile', message='A message')

        # Bad request for 'put' compared to 'patch' (because we need 'message' field for the Anwer but not provided)
        bad_data = {'username': self.user.username, 'ticketing_obj': new_ticket.id}
        bad_response = self.client.put(reverse('ticketing:answer-detail', kwargs={'pk': self.answer.id}), data=bad_data)
        self.assertEqual(bad_response.status_code, status.HTTP_400_BAD_REQUEST)

        # Now add 'message' for the AnswerSeraializer and Answer model 'message' field required for totally update
        new_data = {'username': self.user.username, 'ticketing_obj': new_ticket.id, 'message': 'New message'}
        response = self.client.put(reverse('ticketing:answer-detail', kwargs={'pk': self.answer.id}), data=new_data)

        # Refresh answer object to show new data
        self.answer.refresh_from_db()

        serializer = AnswerSerializer(instance=self.answer, many=False, context={'request': self.request})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serializer.data)
        self.assertNotEqual(self.answer.ticketing.title, old_ticket_title)
    
    def test_answer_delete_api(self):
        """Test if we can delete an answer with api"""
        self.assertIsNotNone(Answer.objects.filter(id=self.answer.id).last())

        response = self.client.delete(path=reverse('ticketing:answer-detail', kwargs={'pk': self.answer.id}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(Answer.objects.filter(id=self.answer.id).last())
