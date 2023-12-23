from django.shortcuts import render, redirect
from accounts.forms import UserForm
from accounts.models import User, UserProfile
from django.contrib import messages, auth
from vendor.forms import VendorForm
from vendor.utils import detectUser, send_verification_email
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, user_passes_test

def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied
    
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied
    
# from django.core.mail import send_mail

# send_mail(
#     subject="Test email",
#     message="This is a test email sent from Django.",
#     from_email="rino.setiyo@gmail.com",
#     recipient_list=["developer.rino@gmail.com"],
# )

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

            # send verification email
            send_verification_email(request, user)

            messages.success(request,'you just registered as CUSTOMER')
            return redirect('registerUser')
    else:
        form = UserForm()
    context = {
        'form':form,
    }
    return render(request, 'accounts/register-user.html', context)

def activate(request, uidb64, token):
    try:
        uid= urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Conratulation your account is activated')
        # return redirect('myAccount')
        return render(request, 'accounts/emails/activation-completed.html')
    else:
        messages.error(request, 'invalid activation link')
        # return redirect('myAccount')
    
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

            # send verification email
            mail_subject = "activation email"
            email_templates = "accounts/emails/account_verification_email.html"
            send_verification_email(request, user, mail_subject, email_templates)

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

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "you just login")
            return redirect('myAccount')
        else:
            messages.error(request, 'login error')
            return redirect('login')
        
    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, 'you just logged out')
    return redirect('login')

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, 'vendors/vendor-dashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request, 'customers/customer-dashboard.html')

def forget_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            mail_subject = "reset password"
            email_templates = "accounts/emails/reset_password.html"
            send_verification_email(request, user, mail_subject, email_templates)

            messages.success(request, 'password reset link has been send')
            return redirect('login')
        else:
            messages.error(request, 'account does not exist')
    return render(request, 'accounts/forget_password.html')

def reset_password_validate(request, uidb64, token):
    try:
        uid= urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'invalid activation link')
        # return redirect('myAccount')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'password do not match')
            return redirect('reset_password')
    return render(request, 'accounts/reset_password.html')