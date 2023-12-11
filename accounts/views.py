from django.shortcuts import render, redirect
from accounts.forms import UserForm
from accounts.models import User, UserProfile
from django.contrib import messages
from vendor.forms import VendorForm

# Create your views here.
def registerUser(request):
    if request.POST:
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.role = User.CUSTOMER
            user.set_password(password)
            user.save()
            messages.success(request,'you just registered as CUSTOMER')
            return redirect('registerUser')
    else:
        form = UserForm()
    context = {
        'form':form,
    }
    return render(request, 'accounts/register-user.html', context)

def registerVendor(request):
    if request.POST:
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid:
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.role = User.RESTAURANT
            user.set_password(password)
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, "you just registered as VENDOR")
            return redirect('registerVendor')
    else:
        form = UserForm()
        v_form = VendorForm()
    context = {
        'form':form,
        'v_form':v_form,
    }
    return render(request, 'accounts/register-restaurant.html', context)