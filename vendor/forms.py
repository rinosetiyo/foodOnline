from django import forms
from vendor.models import Vendor


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['profile_picture','cover_photo','vendor_name', 'vendor_license']