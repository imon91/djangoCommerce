from django.conf import settings
from django.db import models


# Create your models here.

class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, blank=True, null=True)
    zipcode = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    contry = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'{self.user.profile.username}'

    def is_fully_fill(self):
        fields_names = [f.name for f in self._meta.get_fields()]
        for fields_name in fields_names:
            value = getattr(self, fields_name)
            if value is None or value == '':
                return False

        return True
