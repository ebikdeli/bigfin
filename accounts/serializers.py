from rest_framework import serializers
from .models import User

from .models import Address


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'name', 'is_active',
                  'is_staff', 'is_admin']


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'
