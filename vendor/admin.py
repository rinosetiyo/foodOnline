from django.contrib import admin
from vendor.models import Vendor
from django.contrib.auth.admin import UserAdmin

# Register your models here.
# class CustomVendorAdmin(UserAdmin):
#     list_display = ('username', 'vendor_name', 'vendor_license', 'is_approved')

admin.site.register(Vendor)