from django.shortcuts import render, redirect
from accounts.forms import UserForm
from accounts.models import User
from django.contrib import messages

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
            messages.success(request,'you just registered as customer')
            return redirect('registerUser')
    else:
        form = UserForm()
    context = {
        'form':form,
    }
    return render(request, 'accounts/register-restaurant.html', context)