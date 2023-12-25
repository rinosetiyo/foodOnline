from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import UserProfile
from vendor.models import Vendor
from accounts.forms import UserProfileForm
from vendor.forms import VendorForm
from django.contrib import messages
# Create your views here.

def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)
    profile_form = UserProfileForm()
    vendor_form = VendorForm()
    
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid and vendor_form.is_valid:
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'settings updated')
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)
    context = {
        'profile':profile,
        'vendor':vendor,
        'profile_form': profile_form,
        'vendor_form' : vendor_form,
    }
    return render(request, 'vendor/vprofile.html', context)