"""
If we have a file in our serializer, we must set 'format' argument in APIClient() 'post', 'put' and 'patch'
methods to 'multipart'. This argument defaulted to 'json'
for eg: self.client.post(path=..., data=..., format='multipart')

In this module there is a test method with this address:
    'TestFileUpload.test_file_upload_content_type_inner_serializer_valid_with_api'
that we implemented bad structured but with good practical test!
Documents used in this module:
https://docs.djangoproject.com/en/4.0/ref/contrib/contenttypes/#methods-on-contenttype-instances
https://www.django-rest-framework.org/api-guide/relations/#nested-relationships
https://www.django-rest-framework.org/api-guide/fields/#listfield
https://www.django-rest-framework.org/api-guide/fields/#file-upload-fields
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
from html5lib import serialize
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
        # IMPORTANT: 'format' argument in below line is defaulted to 'json'. But if we have a 'file' or 'image' or
        # any other type of file, we must set format is 'multipart'.
        response_user_obj = self.client.post(path=reverse('ticketing:ticketing-list'),
                                             data=ticket_data_user_obj,
                                             format='json')
        self.assertEqual(response_user_obj.status_code, status.HTTP_201_CREATED)

        # Create ticket using 'username' field:
        ticket_data_username = {'username': self.user.username, 'title': 'This is title', 'message': 'This is message'}
        response_username = self.client.post(reverse('ticketing:ticketing-list'), data=ticket_data_username)
        self.assertEqual(response_username.status_code, status.HTTP_201_CREATED)

        # Creating using both 'user_obj' and 'username' field:
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
    
    def test_answer_list_query_params_api(self):
        """
        We should test it in 'list' action of 'AnswerViewset' and see how 'request.query_params' works
        and how we can use it to filter queryset
        """
        response = self.client.get(path=reverse('ticketing:answer-list')+'?name=ehsan&age=30')
        # Or we should set 'data' argument of our action method. If we use 'data' argument,
        # anything comes after '?' will be skipped:
        # response = self.client.get(path=reverse('ticketing:answer-list'), data={'name': 'ehsan', 'age': 30})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
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
    
    def test_answer_create_bad_api(self):
        """Test effect of bad request on the post method"""
        # 'post' method only accepts 'serializable data' not arbitrary objects such as 'User' and 'Ticket'
        bad_data = {'user_obj': self.user, 'ticketing_obj': self.ticket, 'message': 'Bad request'}
        response = self.client.post(reverse('ticketing:answer-list'), data=bad_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        serializer = AnswerSerializer(Answer.objects.last(), many=False, context={'request': self.request})

        self.assertNotEqual(response.json(), serializer.data)
    
    def test_answer_create_api(self):
        """Test if new answer created properly"""
        # We can get 'ticket' object for creating answer in 4 ways with 4 fields in the AnswerSerializer:
        # 1- Using 'user_obj' and 'ticketing_obj'
        # 2- Using 'username' and 'ticketing_obj'
        # 3- Using 'user_obj' and 'ticket_id'
        # 4- Using 'username' and 'ticket_id'
        # We can use any way we want but remember that for 'user_obj' and 'ticketing_obj' we need to get
        # them with 'lookup_field' or in this case the field is 'id':
        answer_data_1 = {'user_obj': self.user.id, 'ticket_id': self.ticket.ticket_id, 'message': 'This is message answer'}
        response_1 = self.client.post(reverse('ticketing:answer-list'), data=answer_data_1)
        self.assertEqual(response_1.status_code, status.HTTP_201_CREATED)

        # serializer = AnswerSerializer(instance=Answer.objects.last(), many=False, context={'request': self.request})
        # Below line to show how to send extra data to Serializer for future use:
        serializer = AnswerSerializer(instance=Answer.objects.last(),
                                      many=False,
                                      context={'request': self.request, 'name': 'ehsan', 'age': 30})

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


class TestFileUpload(TestCase):
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

        # Create two UploadFiles for Ticket and Answer
        upload_file_data_ticket = {'content_object': self.ticket,
                                   'file': SimpleUploadedFile(name='file_1.txt', content=b'file_1 contents'),
                                   'caption': 'This is ticket file caption'}
        upload_file_data_answer = {'content_object': self.answer,
                                   'file': SimpleUploadedFile(name='file_2.jpg', content=b'file_2 contents'),
                                   'caption': 'This is answer file caption'}
        self.file_ticket = FileUpload.objects.create(**upload_file_data_ticket)
        self.file_answer = FileUpload.objects.create(**upload_file_data_answer)
    
    def test_fileupload_content_type_inner_serializer_valid_with_api(self):
        """
        THIS TEST IS SPECIAL. It has many things to learn from. From how to send data via serializer without any instance
        to how to create new object from ContentType model directly programmatically, From validating serializer and save
        and creating new object to how sending data to 'List fields' in serializers and a nested serializer as child
        serializer!.
        """
        # 'model' argument in ContentType queryset must be 'lowercase' even if the class is 'TitleCase':
        cont_type = ContentType.objects.get(model='answer')
        # print(cont_type.id)
        cont_obj = cont_type.get_object_for_this_type(id=self.answer.id)
        # print(cont_type.name)
        # print(cont_obj.id)
        """In the AnswerSerializer we defined a field name 'files_upload' that its value is 'FileUploadSerializer'.
        This means if want to set value for 'files_upload' field, must be a value we would send to FileUploadSerializer
        like what we do with 'file_data_1'"""
        file_data_1 = {# 'content_object': self.answer.id,
                       'content_type': cont_type.id,
                       'object_id': cont_obj.id,
                       'file': SimpleUploadedFile(name='file_3.jpg', content=b'file_3 contents'),
                       'caption': 'This is answer file 3 caption'}
        file_data_2 = {# 'content_object': self.answer.id,
                       'content_type': cont_type.id,
                       'object_id': cont_obj.id,
                       'file': SimpleUploadedFile(name='file_4.jpg', content=b'file_4 contents'),
                       'caption': 'This is answer file 4 caption'}

        # print(SimpleUploadedFile(name='file_3.jpg', content=b'file_3 contents'))
        #s = FileUploadSerializer(data=file_data_1)
        # https://stackoverflow.com/questions/46805662/collections-ordereddict-object-has-no-attribute-pk-django-rest-framework
        #s.is_valid()
        #print(s)
        #print(s.validated_data)

        s1 = FileUploadSerializer(data=file_data_1, context={'request': self.request})
        s1.is_valid()
        # We can save the serializer and create new object (FileUpload)
        s1.save()

        s2 = FileUploadSerializer(data=file_data_2, context={'request': self.request})
        s2.is_valid()
        s2.save()

        answer_data = {'user_obj': self.user.id, 'ticketing_obj': self.ticket.id, 'message': 'This is Answer message'}
        answer_data.update({'files_upload': [file_data_1, file_data_2]})
        kwargs = {'name': 'ehsan', 'age': 30}
        serializer = AnswerSerializer(data=answer_data, context={'request': self.request})
        serializer.is_valid()
        serializer.save()
    

    def test_fileupload_list_api(self):
        """Test if fileupload serializer works properly"""
        f1_data = {'file': SimpleUploadedFile(name='file1.jpg', content=b'file 1 contents')}
        f2_data = {'file': SimpleUploadedFile(name='file2.jpg', content=b'file 2 contents')}
        
        f1, f2 = FileUpload.objects.bulk_create([FileUpload(**f1_data), FileUpload(**f2_data)])
        self.assertTrue(f1.file)
        self.assertTrue(f2.file)

        response = self.client.get(reverse('ticketing:fileupload-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = FileUploadSerializer(instance=FileUpload.objects.all(), many=True, context={'request': self.request})

        self.assertEqual(serializer.data, response.json())
    
    def test_fileupload_retreive_api(self):
        """Test if retreive fileupload properly using api"""
        response = self.client.get(reverse('ticketing:fileupload-detail', kwargs={'pk': self.file_answer.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = FileUploadSerializer(instance=self.file_answer, many=False, context={'request': self.request})

        self.assertEqual(response.json(), serializer.data)
    
    def test_fileupload_create_bad_api(self):
        """Test effect of bad request on the post method"""
        # 'post' method only accepts 'serializable data' not arbitrary objects such as 'file' or 'content_type'
        bad_data = {'file': 'bad file', 'content_type': -10, 'caption': 'Bad request'}
        response = self.client.post(reverse('ticketing:fileupload-list'), data=bad_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        serializer = FileUploadSerializer(FileUpload.objects.last(), many=False, context={'request': self.request})

        self.assertNotEqual(response.json(), serializer.data)
    
    def test_fileupload_create_api(self):
        """Test if new fileupload created properly"""
        # We can create fileupload for any content_type we want (Or we can don't set content_type!). But in this test we use 'self.file_ticketing'
        cont = ContentType.objects.get(model='ticketing')
        upload_file_data = {'file': SimpleUploadedFile(name='file.exe', content=b'data'), 'content_type': cont.id, 'object_id': self.ticket.id, 'caption': 'This is caption'}

        response_1 = self.client.post(reverse('ticketing:fileupload-list'), data=upload_file_data)
        self.assertEqual(response_1.status_code, status.HTTP_201_CREATED)

        serializer = FileUploadSerializer(instance=FileUpload.objects.last(), many=False, context={'request': self.request})

        self.assertEqual(response_1.json(), serializer.data)

        # Making another fileupload for fun but this time with 'self.file_answer'
        cont2 = ContentType.objects.get(model='answer')
        upload_file_data_ticket = {'file': SimpleUploadedFile(name='file2.exe', content=b'data2'), 'content_type': cont2.id, 'object_id': self.answer.id, 'caption': 'This is caption'}
        response_2 = self.client.post(reverse('ticketing:fileupload-list'), data=upload_file_data_ticket)

        self.assertEqual(response_2.status_code, status.HTTP_201_CREATED)
        
    def test_fileupload_partially_update_api(self):
        """Test 'patch' method to partially update an fileupload with api"""
        # Test current file_answer file of the answer
        old_fileupload_file = self.file_answer.file
        self.assertEqual(self.file_answer.file, old_fileupload_file)

        new_data = {'file': SimpleUploadedFile(name='file3.exe', content=b'data3'), 'caption': 'Some caption'}
        response = self.client.patch(reverse('ticketing:fileupload-detail', kwargs={'pk': self.file_answer.id}), data=new_data)

        # Refresh self.file_answer object to show new data
        self.file_answer.refresh_from_db()

        serializer = FileUploadSerializer(instance=self.file_answer, many=False, context={'request': self.request})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serializer.data)
        self.assertNotEqual(self.file_answer.file, old_fileupload_file)
    
    def test_fileupload_totally_update_api(self):
        """Test 'put' method to totally update an fileupload with api"""
        # Test current fileupload caption. We are using 'self.file_ticket' for this test
        old_file_ticket_caption = self.file_ticket.caption
        self.assertEqual(self.file_ticket.caption, old_file_ticket_caption)

        # Bad request for 'put' method because we don't provide 'content_type':
        bad_data = {'file': SimpleUploadedFile(name='file3.exe', content=b'data3'), 'caption': 'Some caption'}
        bad_response = self.client.put(reverse('ticketing:fileupload-detail', kwargs={'pk': self.file_ticket.id}), data=bad_data)
        self.assertEqual(bad_response.status_code, status.HTTP_400_BAD_REQUEST)

        # We have to provide completly new data for the self.file_ticket as oppose to 'patch' method
        cont = ContentType.objects.get(model='ticketing')
        new_data = {'file': SimpleUploadedFile(name='file4.exe', content=b'data4'),
                    'content_type': cont.id,
                    'object_id': self.file_ticket.id,
                    'caption': 'New message'}
        response = self.client.put(reverse('ticketing:fileupload-detail', kwargs={'pk': self.file_ticket.id}), data=new_data)

        # Refresh fileupload object to show new data
        self.file_ticket.refresh_from_db()

        serializer = FileUploadSerializer(instance=self.file_ticket, many=False, context={'request': self.request})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serializer.data)
        self.assertNotEqual(self.file_ticket.caption, old_file_ticket_caption)
    
    def test_fileupload_delete_api(self):
        """Test if we can delete an fileupload with api"""
        # In this case we selected 'fiel_answer' to delete
        self.assertIsNotNone(FileUpload.objects.filter(id=self.file_answer.id).last())

        response = self.client.delete(path=reverse('ticketing:fileupload-detail', kwargs={'pk': self.file_answer.id}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(FileUpload.objects.filter(id=self.file_answer.id).last())
