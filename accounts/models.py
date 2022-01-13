from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator, MaxLengthValidator, MinLengthValidator


class MyUserManager(BaseUserManager):
    """Create custom user manager for our custom User"""
    def create_user(self, phone, password=None, name=None, **kwargs):
        """
        Creates and saves a User with the given email and password.
        """
        if not phone:
            raise ValueError(_('Users must have an phone number'))

        # actually below line is this <==> user = User(email=User.objects.normalize_email(email), password=password)
        user = self.model(
            phone=phone,
            password=password,
            name=name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, name=None, **kwargs):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            phone,
            password=password,
            name=name,
        )
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=13,
                             unique=True,
                             verbose_name=_('phone'),
                             validators=[MaxLengthValidator(13, _('phone number is too long')),
                                         MinLengthValidator(11, _('phone number length is too short'))],
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
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    slug = models.SlugField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = MyUserManager()
    
    USERNAME_FIELD = 'phone'

    def __str__(self) -> str:
        return self.phone
    
    def get_absolute_url(self):
        # return reverse("model_detail", kwargs={"pk": self.pk, "slug": self.slug})
        # OR
        # return reverse('model_detail', self.pk, self.slug))
        pass
