from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('marketplace/', views.marketplace, name='marketplace'),
    path('marketplace/vendor_detail/<int:pk>', views.vendor_detail, name='vendor_detail'),
]