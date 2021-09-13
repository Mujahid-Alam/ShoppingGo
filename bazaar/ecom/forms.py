from django import forms
from ecom.models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ("user",)

