from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.
class MyUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("please set mail")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError("please set is_staff")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("please set is_superuser")
        if extra_fields.get('is_active') is not True:
            raise ValueError("please set is_active")
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False)
    is_staff = models.BooleanField(
        ugettext_lazy('staff_status'),
        default=False,
        help_text=ugettext_lazy('user can log in this site')
    )
    is_active = models.BooleanField(

        ugettext_lazy('is_active'),
        default=True,
        help_text=ugettext_lazy('user should be active')

    )
    USERNAME_FIELD = 'email'
    object = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=200, blank=True)
    fullname = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    postcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    address = models.TextField(max_length=200, blank=True)
    datejoin = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username + "'s Profile"

    def is_fully_fill(self):
        fields_names = [f.name for f in self._meta.get_fields()]
        for fields_name in fields_names:
            value = getattr(self, fields_name)
            if value is None or value == '':
                return False

        return True


@receiver(post_save, sender=User)
def create_profile(instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
