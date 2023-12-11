from django.urls import path
from accounts import views

urlpatterns = [
    path('register-user/', views.registerUser, name='registerUser'),
    path('register-vendor/', views.registerVendor, name='registerVendor'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]