from django.urls import path
from accounts import views

urlpatterns = [
    path('register-user/', views.registerUser, name='registerUser'),
]