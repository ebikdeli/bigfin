"""
Unlike Models and signals that we should use 'settings.AUTH_USER_MODEL' instead of 'get_user_model' method,
in serializers and filtersets we can't use 'AUTH_USER_MODEL' or stringized <app_name.Model_Name>' or we get
this error:
AttributeError: 'str' object has no attribute '_meta'
"""
from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model

from .models import Address


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for User model"""
    url = serializers.HyperlinkedIdentityField(view_name='accounts:user-detail')

    class Meta:
        # model = settings.AUTH_USER_MODEL  <==> This is wrong! We should use below command instead:
        model = get_user_model()
        fields = ['url', 'username', 'email', 'name', 'is_active',
                  'is_staff', 'is_admin', 'is_superuser',
                  'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class AddressSerializer(serializers.ModelSerializer):
    """Serializer for Address model"""
    url = serializers.HyperlinkedIdentityField(view_name='accounts:address-detail')

    class Meta:
        # model = 'accounts.Address'    <==> This command is wrong! We should below line instead:
        model = Address
        fields = '__all__'
