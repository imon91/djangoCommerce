from django.forms import ModelForm
from django import forms

from app_payment.models import BillingAddress


class BllingForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = ['address','zipcode','city','contry']