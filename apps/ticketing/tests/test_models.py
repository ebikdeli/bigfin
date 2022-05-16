"""
Documents used for this module:
1- https://docs.djangoproject.com/en/4.0/ref/contrib/contenttypes/#generic-relations
2- https://docs.djangoproject.com/en/4.0/ref/contrib/contenttypes/#reverse-generic-relations
3- https://docs.djangoproject.com/en/4.0/ref/forms/api/#binding-uploaded-files-to-a-form
4- https://stackoverflow.com/questions/4283933/what-is-the-clean-way-to-unittest-filefield-in-django
5- https://docs.djangoproject.com/en/4.0/topics/db/examples/many_to_one/
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from ticketing.models import Ticketing, Answer, FileUpload


class TestTicketing(TestCase):
    def setUp(self) -> None:
        user_kwargs = {'username': 'customer', 'password': '123456', 'email': 'customer@gmail.com'}
        self.user = get_user_model().objects.create(**user_kwargs)

    def test_ticketing_create_delete(self):
        """Test if Ticketing model create and delete properly"""
        t_data = {'user': self.user, 'title': 'Ticketing test', 'message': 'This is a testing ticket'}
        # Create a ticket
        ticket = Ticketing.objects.create(**t_data)
        self.assertEqual(ticket.emergency, '3')

        # Delete the ticket
        Ticketing.objects.filter(ticket_id=ticket.ticket_id).delete()
        self.assertFalse(Ticketing.objects.filter(pk=ticket.pk).exists())

    def test_ticketing_fileupload_create_indirectly(self):
        """Test if 'file' as Generic relation works okay with Ticketing"""
        # This test shows How it's easy to work with Content types
        t_data = {'user': self.user, 'title': 'Ticketing test', 'message': 'This is a testing ticket'}
        # Create some tickets
        ticket_1 = Ticketing.objects.create(**t_data)
        ticket_2 = Ticketing(**t_data)
        ticket_2.title = 'Another ticketing test'
        ticket_2.save()
        # Create some files
        f1 = FileUpload.objects.create(content_object=ticket_1,
                                       file=SimpleUploadedFile(name='file1.txt', content=b'some data in it'),
                                       caption='this is caption')
        f2 = FileUpload.objects.create(content_object=ticket_1,
                                       file=SimpleUploadedFile(name='file2.jpg', content=b'Image in it'),
                                       caption='Image caption')
        f3 = FileUpload.objects.create(content_object=ticket_2,
                                       file=SimpleUploadedFile(name='file3.jpg', content=b'File for ticket 2'),
                                       caption='caption for ticket 3')

        self.assertEqual(f2, ticket_1.files.filter(pk=f2.pk).last())
        self.assertIn(f1, ticket_1.files.all())
        self.assertEqual(f3.caption, ticket_2.files.last().caption)

    def test_ticketing_file_create_directly(self):
        """Test if files could be created directly by Ticketing properly"""
        t_data = {'user': self.user, 'title': 'Ticketing test', 'message': 'This is a testing ticket'}
        # Create a ticket
        ticket = Ticketing.objects.create(**t_data)
        # Create some FileUpload objects from ticket object directly
        f_1 = ticket.files.create(file=SimpleUploadedFile(name='word.txt', content=b'some text'), caption='text file')
        f_2 = ticket.files.create(file=SimpleUploadedFile(name='book.png', content=b'data'), caption='image file')

        self.assertIn(f_1, ticket.files.all())
        self.assertIn(f_2, ticket.files.filter(pk=f_2.id))
        self.assertEqual(f_2.caption, ticket.files.filter(caption='image file').first().caption)


class TestAnswer(TestCase):
    def setUp(self) -> None:
        user_kwargs = {'username': 'customer', 'password': '123456', 'email': 'customer@gmail.com'}
        admin_kwargs = user_kwargs.copy()
        admin_kwargs.update({'username': 'admin', 'email': 'admin@gmail.com', 'is_staff': True})
        self.user = get_user_model().objects.create(**user_kwargs)
        self.admin = get_user_model().objects.create(**admin_kwargs)
        t_data = {'title': 'some title', 'message': 'this ticket is for testing purpose'}
        self.ticket = Ticketing.objects.create(**t_data, user=self.user)

    def test_create_delete_answer(self):
        """Test if Answer successfully created or deleted"""
        # Remember that empty queryset is not a None type object
        msg = 'This is customer answer'
        # Create answer
        answer = Answer.objects.create(ticketing=self.ticket, user=self.user, message=msg)

        self.assertEqual(answer.message, msg)
        self.assertEqual(answer.user, self.ticket.user)
        # Delete the Answer
        Answer.objects.filter(pk=answer.pk).delete()

        self.assertIsNone(Answer.objects.filter(pk=answer.id).last())

    def test_answer_fileupload_create_indirectly(self):
        """Test if 'file' as Generic relation works okay with Answer"""
        # This test shows How it's easy to work with Content types
        a_data = {'user': self.user, 'ticketing': self.ticket, 'message': 'This is a testing ticket'}
        # Create some answers
        answer_1 = Answer.objects.create(**a_data)
        answer_2 = Answer(**a_data)
        answer_2.message = 'Another Answer test'
        answer_2.save()
        # Create some files
        f1 = FileUpload.objects.create(content_object=answer_1,
                                       file=SimpleUploadedFile(name='file1.txt', content=b'some data in it'),
                                       caption='this is caption')
        f2 = FileUpload.objects.create(content_object=answer_1,
                                       file=SimpleUploadedFile(name='file2.jpg', content=b'Image in it'),
                                       caption='Image caption')
        f3 = FileUpload.objects.create(content_object=answer_2,
                                       file=SimpleUploadedFile(name='file3.jpg', content=b'File for ticket 2'),
                                       caption='caption for ticket 3')

        self.assertEqual(f2, answer_1.files.filter(pk=f2.pk).last())
        self.assertIn(f1, answer_1.files.all())
        self.assertEqual(f3.caption, answer_2.files.last().caption)

    def test_answer_file_create_directly(self):
        """Test if files could be created directly by Answer properly"""
        a_data = {'user': self.user, 'ticketing': self.ticket, 'message': 'This is a testing ticket'}
        # Create a answer
        answer = Answer.objects.create(**a_data)
        # Create some FileUpload objects from answer object directly
        f_1 = answer.files.create(file=SimpleUploadedFile(name='word.txt', content=b'some text'),caption='text file')
        f_2 = answer.files.create(file=SimpleUploadedFile(name='book.png', content=b'data'), caption='image file')

        self.assertIn(f_1, answer.files.all())
        self.assertIn(f_2, answer.files.filter(pk=f_2.id))
        self.assertEqual(f_2.caption, answer.files.filter(caption='image file').first().caption)

    def test_ticketing_is_answered_flag(self):
        """Test if 'admin' answered a ticket, the 'is_answered' would changed to True"""
        # 1- created ticket should not have 'True' flag for its answered
        self.assertFalse(self.ticket.is_answered)

        # 2- Answer created by 'admin' user should change the flag
        answered_admin = Answer.objects.create(user=self.admin, ticketing=self.ticket, message='ticket just answered')
        self.assertTrue(self.ticket.is_answered)

        # 3- Then customer create another answer and ticket 'is_answered' flag turns to False
        answered_customer = Answer.objects.create(user=self.user, ticketing=self.ticket, message='customer answered')
        self.assertFalse(self.ticket.is_answered)

        # 4- And admin again answering to customer and 'is_answered' flag turns to True again!
        answered_admin_again = Answer.objects.create(user=self.admin, ticketing=self.ticket, message='Fuck you!')
        self.assertTrue(self.ticket.is_answered)
