from django.urls import path
from vendor import views

urlpatterns = [
    path('my_restaurant/', views.vprofile, name='vprofile'),
]