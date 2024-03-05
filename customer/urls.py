from django.urls import path
from customer import views

urlpatterns = [
    path('cprofile', views.cprofile, name='cprofile'),
]