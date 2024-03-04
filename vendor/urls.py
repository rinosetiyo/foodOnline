from django.urls import path
from vendor import views

urlpatterns = [
    path('my_restaurant/', views.vprofile, name='vprofile'),
    path('menu_builder/', views.menu_builder, name='menu_builder'),
    path('menu_builder/fooditems/<int:pk>', views.fooditems_by_category, name='fooditems'),

    path('menu_builder/add_category/', views.add_category, name='add_category'),
    path('menu_builder/edit_category/<int:pk>', views.edit_category, name='edit_category'),
    path('menu_builder/delete_category/<int:pk>', views.delete_category, name='delete_category'),

    path('menu_builder/fooditems/add_fooditem', views.add_fooditem, name='add_fooditem'),
    path('menu_builder/fooditems/edit_fooditem/<int:pk>', views.edit_fooditem, name='edit_fooditem'),
    path('menu_builder/fooditems/delete_fooditem/<int:pk>', views.delete_fooditem, name='delete_fooditem'),

    path('opening_hours/', views.opening_hours, name='opening_hours'),
    path('add_opening_hours/', views.add_opening_hours, name='add_opening_hours'),
    path('remove_opening_hours/<int:pk>', views.remove_opening_hours, name='remove_opening_hours'),
]