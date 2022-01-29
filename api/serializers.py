import imp
from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.models import Address
from currency.models import Currency
from wallet.models import Wallet


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer used for Users"""
    url = serializers.HyperlinkedIdentityField(view_name='some view')

    class Meta:
        model = get_user_model()
        include = ['username', 'password', 'email', 
                   'name', 'is_admin', 'picture',
                   'score', 'is_superuser', 'is_active']


class UserAddress(serializers.HyperlinkedModelSerializer):
    """Serializer used for user Address"""
    url = serializers.HyperlinkedIdentityField(view_name='some view')

    class Meta:
        model = Address
        include = '__all__'


class CurrencySerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Currency"""
    url = serializers.HyperlinkedIdentityField(view_name='some view')

    class Meta:
        model = Currency
        include = '__all__'


class WalletSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Wallet"""
    url = serializers.HyperlinkedIdentityField(view_name='some view')

    class Meta:
        model = Wallet
        include = '__all__' 
