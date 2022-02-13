"""
To test apis we should have views and urls and use diffrent http methods to retreive or create or update models.
1- We get our reverse url address based on following document:
https://www.django-rest-framework.org/api-guide/routers/#defaultrouter
2- To be able to simulate 'request' object we use these documents:
https://docs.djangoproject.com/en/4.0/topics/testing/advanced/#the-request-factory
https://www.django-rest-framework.org/api-guide/testing/#apirequestfactory

3- Because we use Serializer inheritance for User model serializer in the VIEWs, We must use UserNewSerializer
for test. Actually we should use the child serializer for everything.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework import status

from accounts.models import Address
from accounts.serializers import UserNewSerializer, UserSerializer, AddressSerializer


def get_lookup_field_value(user_obj):
    """
    This function used to be able to work with any arbitrary 'lookup_field' from UserViewSet. This is
    help us to change 'lookup_field' without the need to change test codes!
    https://stackoverflow.com/questions/21945067/how-to-list-all-fields-of-a-class-and-no-methods
    https://stackoverflow.com/questions/3647805/get-models-fields-in-django
    """
    from accounts.views import UserViewSet
    # 'lookup_field' is an attribute in UserViewSet class
    lookup_field = UserViewSet.lookup_field
    if lookup_field == 'pk':
        data = {'pk': user_obj.id}
    else:
        # With '__dict__' dunder magic method we can get all the attributes and their value of any object in python!
        user_field = user_obj.__dict__.get(lookup_field, None)
        data = {lookup_field: user_field}
    return data


class TestUserSerializer(TestCase):
    def setUp(self) -> None:
        user_data = {'username': 'reza', 'password': '1234567'}
        admin_data = {'username': 'ehsan', 'password': '123456'}

        self.user = get_user_model().objects.create_user(**user_data)
        self.admin = get_user_model().objects.create_superuser(**admin_data)
        self.client = APIClient()

        self.kwargs = get_lookup_field_value(self.admin)

    def test_user_api_list(self):
        """Test if user list could be reached by API"""
        # Get user data with api
        # If we use 'login' method for the client we should provide credentials like username, email, phone, password #
        self.client.force_login(self.admin)     # We should login as an admin user
        # NOTE: 2 following commands are same but the seconde is more standard #
        # response = self.client.get(f'/accounts/user/')
        response = self.client.get(reverse('accounts:user-list'))

        # Get user data from serializer
        # NOTE: First we should simulate 'request' object for the HyperllinkedModelSerializer or if there
        # are needs that we should provide the 'request' object for our serializer:
        request = APIRequestFactory().get(reverse('accounts:user-list'))
        user_list = UserNewSerializer(get_user_model().objects.all(), many=True, context={'request': request})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user_list.data, response.json())
    
    def test_user_api_retreive(self):
        """Test if we can retreive a user with api"""
        # Get user with api
        self.client.force_login(self.admin)
        # NOTE: 2 following commands are same but the seconde is more standard #
        # response = self.client.get(f'/accounts/user/{self.admin.id}/')
        # response = self.client.get(reverse('accounts:user-detail', kwargs={'pk': self.admin.id}))

        # MORE GENERIC API FOR EVERY USERNAME_FIELD WE WANT:
        response = self.client.get(reverse('accounts:user-detail', kwargs=self.kwargs))

        # Get the same user with serializer
        request = APIRequestFactory().get(reverse('admin:index'))   # It's not much matter where we get request!?
        serializer = UserNewSerializer(self.admin, many=False, context={'request': request})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serializer.data)
    
    def test_user_api_unauthorized(self):
        """
        Test if unauthorized users can't access to user list, retreive, post or update.
        NOTE: We just use user list to test the program but it doesn't diffrent for other methods.
        """
        # First test any unauthenticated user can reach to secured resources
        response = self.client.get(reverse('accounts:user-list'))

        # If 'permission_classes' of the viewset set to 'IsAdmin' we use this:

        # self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # If 'permission_classes' of the viewset set to 'IsAdmin' we use this:
        # self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # This time test if unauthorized user without enough access could access secured resources
        # self.client.force_login(self.user)
        # response = self.client.get(reverse('accounts:user-list'))
        # self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_user_api(self):
        """Test if we can create a user using api"""
        self.client.login(username=self.admin.username, password='123456')
        # First create a new user and test if it created
        user_data = {'username': 'ali', 'password': '12345678', 'is_staff': True}
        response = self.client.post(reverse('accounts:user-list'), data=user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Then we test if newly created user could be reached via serializer
        new_user_data = response.json()
        new_user = get_user_model().objects.get(username=new_user_data['username'])
        request = APIRequestFactory().get(reverse('admin:index'))
        serializer = UserNewSerializer(instance=get_user_model().objects.get(username=new_user_data['username']),
                                       many=False,
                                       context={'request': request})

        self.assertEqual(serializer.data, response.json())
        self.assertEqual(new_user.username, serializer.data['username'])
    
    def test_partial_update_user_api(self):
        """
        Test if user could get partial updated by api. Partial update means we should use 'patch' method.
        Note that after updating an object in the database, we should REFRESH the object from data base
        to be able to see the changes.
        """
        # First we check if 'is_staff' flag is False and 'name' is None
        self.assertEqual(self.user.is_staff, False)
        self.assertIsNone(self.user.name)

        self.client.force_login(self.admin)
        new_data = {'is_staff': True, 'is_admin': True, 'is_staff': True, 'name': 'ARASH'}
        # response = self.client.patch(path=reverse('accounts:user-detail', kwargs={'pk': self.user.id}), data=new_data)
        response = self.client.patch(path=reverse('accounts:user-detail', kwargs=get_lookup_field_value(self.user)), data=new_data)

        # https://docs.djangoproject.com/en/dev/ref/models/instances/#django.db.models.Model.refresh_from_db
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['is_staff'], True)
        self.assertEqual(self.user.name, 'ARASH')
    
    def test_total_update_user_api(self):
        """Test if user could get total updated by api. This means we should use 'put' method."""
        self.client.force_login(self.admin)
        new_data = {'username': 'reza', 'password': '1234567', 'name': 'reza', 'is_staff': True}
        # response = self.client.put(path=reverse('accounts:user-detail', kwargs={'pk': self.user.id}), data=new_data)
        response = self.client.put(path=reverse('accounts:user-detail', kwargs=get_lookup_field_value(self.user)), data=new_data)

        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.is_staff, True)
        self.assertEqual(self.user.name, 'reza')
        self.assertEqual(response.json()['name'], 'reza')
    
    def test_user_delete_api(self):
        """Test if user could be deleted throught api"""
        self.client.force_login(self.admin)

        # First we test if there user in the data base with arbitrary username
        user = get_user_model().objects.filter(username=self.user.username)
        self.assertIsNotNone(user.last())

        # Then we use delete method to delete the user in database
        # response = self.client.delete(path=reverse('accounts:user-detail', kwargs={'pk': self.user.id}))
        response = self.client.delete(path=reverse('accounts:user-detail', kwargs=get_lookup_field_value(user.last())))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check if the user is not in the database
        no_user = get_user_model().objects.filter(username=self.user.username)
        self.assertIsNone(no_user.last())


class TestAddress(TestCase):
    def setUp(self) -> None:
        # Create a user (Admin)
        user_data = {'username': 'ehsan', 'password': '123456'}
        self.admin = get_user_model().objects.create_superuser(**user_data)

        # Create a client and login the user
        self.client = APIClient()
        self.client.force_authenticate(self.admin)
    
    def test_list_address_api(self):
        """Test if user can get all address list with the api"""
        # First create a couple of Address objects
        address_1 = Address.objects.create(user=self.admin, country='Iran', city='Andimeshk')
        address_2 = Address.objects.create(user=self.admin, country='USA', city='LA')
        
        # Use serializers to get data from the serializer:
        # Remember we should simulate request object first to use it in the serializer
        request = APIRequestFactory().get('admin:index')
        serializer = AddressSerializer(instance=Address.objects.all(), many=True, context={'request': request})

        # Then we get all address objects with api and compare with the serializer data
        response = self.client.get(reverse('accounts:address-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.json())
    
    def test_retreive_address_api(self):
        """Test if user can retreive an address."""
        # Create an address
        address = Address.objects.create(user=self.admin, country='Iran', city='Andimeshk')
        request = APIRequestFactory().get('admin:index')
        serializer = AddressSerializer(instance=address, many=False, context={'request': request})
        
        # Retreive the address
        response = self.client.get(path=reverse('accounts:address-detail', kwargs={'pk': address.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.json())

    def test_create_address_api(self):
        """
        Test if user can create address. Remember if there is a foreign key field in the model, we shoul
        set the field with 'pk' by default or any other field that spicified as 'lookup_field'.
        """
        # First we test if bad data returns bad request:
        bad_data = {'country': 'Iran', 'city': 'Ahwaz'}
        response = self.client.post(path=reverse('accounts:address-list'), data=bad_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test with user_obj (or create address with DRF GUI)
        address_data_user_obj = {'user_obj': self.admin.id, 'country': 'Iran', 'city': 'Ahwaz' }
        response = self.client.post(path=reverse('accounts:address-list'), data=address_data_user_obj)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test with username(or create address with client-server)
        address_data_user_obj = {'username': self.admin.username, 'country': 'Iran', 'city': 'Ahwaz' }
        response = self.client.post(path=reverse('accounts:address-list'), data=address_data_user_obj)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test if both fields provided without any problem
        address_data_user_obj = {'user_obj': self.admin.id, 'username': self.admin.username, 'country': 'Iran', 'city': 'Ahwaz' }
        response = self.client.post(path=reverse('accounts:address-list'), data=address_data_user_obj)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_partial_update_address_api(self):
        """Test parital update of address with 'patch' method"""
        # Create an address with any way we want:
        address_data = {'user': self.admin, 'country': 'Iran', 'city': 'Ahwaz'}
        address = Address.objects.create(**address_data)
        # OR we create address following way:
        # address_data = {'user': self.admin.id, 'country': 'Iran', 'city': 'Ahwaz'}
        # self.client.post(path=reverse('accounts:address-list'), data=address_data)
        self.assertEqual(address.city, 'Ahwaz')

        # It doesn't matter we use 'user_obj' or 'username' to identify 'user' obj for api request
        response = self.client.patch(path=reverse('accounts:address-detail', kwargs={'pk': address.id}),
                                     data={'username': self.admin.username, 'city': 'LA'})
        # Remember to refresh object after every update
        address.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(address.city, 'LA')
    
    def test_total_address_update_api(self):
        """Test if address could be updated totally by api by 'put' method."""
        address_data = {'user': self.admin, 'country': 'Iran', 'city': 'Ahwaz'}
        address = Address.objects.create(**address_data)
        self.assertEqual(address.city, 'Ahwaz')
        self.assertIsNone(address.line)

        new_data = {'user_obj': self.admin.id, 'country': 'Iran', 'city': 'Tehran', 'line': 'Valjar 6'}
        response = self.client.put(path=reverse('accounts:address-detail', kwargs={'pk': address.id}),
                                   data=new_data)
        address.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(address.city, 'Tehran')
        self.assertIsNotNone(address.line)
    
    def test_delete_address_api(self):
        """Test if address could be deleted by api"""
        # Create an Address instance
        address_data = {'user': self.admin, 'country': 'Iran', 'city': 'Ahwaz'}
        address = Address.objects.create(**address_data)

        # Check if created address could be reached
        address_obj = Address.objects.filter(id=address.id)
        self.assertIsNotNone(address_obj.last())

        # Delete the address using api
        response = self.client.delete(reverse('accounts:address-detail', kwargs={'pk': address.id}))
        
        # Check if this address deleted from db
        no_user = Address.objects.filter(id=address.id)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(no_user.last())
