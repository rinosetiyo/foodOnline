from django.contrib import admin
from vendor.models import Vendor, Category, FoodItem, Cart, OpeningHour
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomVendorAdmin(admin.ModelAdmin):
    list_display = ('vendor_name', 'vendor_license', 'is_approved')
    list_editable = ('is_approved',)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ('category_name','vendor','updated_at')
    search_fields = ('category_name',)

class FoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('food_title',)}

class CartAdmin(admin.ModelAdmin):
    list_display = ('user','fooditem','quantity', 'updated_at')

class OpeningHourAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'day', 'from_hour', 'to_hour')

admin.site.register(Vendor, CustomVendorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(FoodItem, FoodItemAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(OpeningHour, OpeningHourAdmin)