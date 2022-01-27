from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator, MaxLengthValidator, MinLengthValidator


class MyUserManager(BaseUserManager):
    """Create custom user manager for our custom User"""
    def create_user(self, username, password=None, name=None, **kwargs):
        """
        Creates and saves a User with the given username and password.
        """
        if not username:
            raise ValueError(_('Users must have an username, email or phone'))

        # actually below line is this <==> user = User(email=User.objects.normalize_email(email), password=password)
        user = self.model(
            username=username,
            password=password,
            name=name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, name=None, **kwargs):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            username,
            password=password,
            name=name,
        )
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=13,
                                unique=True,
                                verbose_name=_('username'),
                                validators=[MaxLengthValidator(33, _('username is too long')),
                                            MinLengthValidator(3, _('username is too short'))],
                                )
    email = models.EmailField(unique=True, verbose_name=_('email'), null=True, blank=True)
    name = models.CharField(verbose_name=_('name'),
                            max_length=50,
                            blank=True,
                            null=True)
    address = models.TextField(verbose_name=_('address'), null=True, blank=True)
    picture = models.ImageField(verbose_name=_('user picture'), blank=True, null=True)
    background = models.ImageField(verbose_name=_('profile background'), blank=True, null=True)
    score = models.IntegerField(verbose_name=_('user score'), default=0)
    score_lifetime = models.IntegerField(verbose_name=_('user life time score'), default=0)
    discount_value = models.DecimalField(verbose_name=_('user discount(value)'), default=0, max_digits=9,
                                         decimal_places=0)
    discount_percent = models.DecimalField(verbose_name=_('user discount(percent)'), default=0, max_digits=5,
                                           decimal_places=2,
                                           validators=[
                                               MaxValueValidator(100, _('percent could not be more than 100')),
                                               MinValueValidator(0, _('percent could not be less than 0'))
                                           ])
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))
    is_staff = models.BooleanField(default=False, verbose_name=_('is staff'))
    is_admin = models.BooleanField(default=False, verbose_name=_('is admin'))
    slug = models.SlugField(blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('updated'))
    objects = MyUserManager()
    
    USERNAME_FIELD = 'username'

    def __str__(self) -> str:
        return self.username
    
    def get_absolute_url(self):
        pass


class Address(models.Model):
    """This model used for comperhensive address usage for user"""
    user = models.ForeignKey(get_user_model(),
                             related_name='user_address',
                             on_delete=models.CASCADE,
                             verbose_name=_('user address'))
    country = models.CharField(verbose_name=_('country'), max_length=50, blank=True, null=True)
    state = models.CharField(verbose_name=_('province, state or municipality'), max_length=50, blank=True, null=True)
    city = models.CharField(verbose_name=_('city'), max_length=50, blank=True, null=True)
    line = models.TextField(verbose_name='line', blank=True, null=True)
    mobile = models.CharField(verbose_name=_('mobile number'), max_length=13, blank=True, null=True,
                              validators=[MaxLengthValidator(13, _('mobile phone cannot be longer than 13 chars')),
                                          MinLengthValidator(11, _('mobile phone cannot be shorter than 11 chars'))])
    phone = models.CharField(verbose_name=_('phone number'), max_length=13, blank=True, null=True,
                             validators=[MaxLengthValidator(13, _('phone cannot be longer than 13 chars')),
                                         MinLengthValidator(11, _('phone cannot be shorter than 11 chars'))])
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('updated'))

    def __str__(self):
        return f'{self.user.username}_address({self.id})'
