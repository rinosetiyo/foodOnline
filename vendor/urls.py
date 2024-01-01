from django.urls import path
from vendor import views

urlpatterns = [
    path('my_restaurant/', views.vprofile, name='vprofile'),
    path('menu_builder/', views.menu_builder, name='menu_builder'),
    path('menu_builder/fooditems/<int:pk>', views.fooditems_by_category, name='fooditems'),
]