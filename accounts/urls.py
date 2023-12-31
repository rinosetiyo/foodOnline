from django.urls import path
from accounts import views

urlpatterns = [
    path('register_user/', views.registerUser, name='registerUser'),
    path('register_vendor/', views.registerVendor, name='registerVendor'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    # password forget and reset
    path('forget_password/', views.forget_password, name='forget_password'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password/', views.reset_password, name='reset_password'),

    # customer and vendor dashboard
    path('myaccount/', views.myAccount, name='myAccount'),
    path('customer/', views.custDashboard, name='custDashboard'),
    path('vendor/', views.vendorDashboard, name='vendorDashboard'),
]