from django import forms
from vendor.models import Vendor



#  Vendor Form provide by Django.
class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']
