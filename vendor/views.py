from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import UserProfile
from vendor.models import Vendor, Category, FoodItem
from accounts.forms import UserProfileForm
from vendor.forms import VendorForm, CategoryForm, FoodItemForm
from django.contrib import messages
from django.template.defaultfilters import slugify
# Create your views here.

def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor

def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)
    
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid and vendor_form.is_valid:
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'settings updated')
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)

    context = {
        'profile':profile,
        'vendor':vendor,
        'profile_form': profile_form,
        'vendor_form' : vendor_form,
    }
    return render(request, 'vendors/vprofile.html', context)

def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor)
    context = {
        'categories':categories,
    }
    return render(request, 'vendors/menu-builder.html', context)

def fooditems_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    fooditems = FoodItem.objects.filter(vendor=vendor, category=category)
    context = {
        'fooditems':fooditems,
        'category':category,
    }
    return render(request, 'vendors/fooditems_by_category.html', context)

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name) + str(category.id)
            category.save()
            messages.success(request, 'category added successfully')
            return redirect('menu_builder')
    else:
        form = CategoryForm()
    context = {
        'form':form,
    }
    return render(request, 'vendors/add_category.html', context)

def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'category updated successfully')
            return redirect('menu_builder')
    else:
        form = CategoryForm(instance=category)
    context = {
        'form':form,
        'category':category,
    }
    return render(request, 'vendors/edit_category.html', context)

def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'category has been deleted successfully')
    return redirect('menu_builder')

def add_fooditem(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            fooditem = form.save(commit=False)
            food_title = form.cleaned_data['food_title']
            fooditem.vendor = get_vendor(request)
            fooditem.slug = slugify(food_title)
            form.save()
            messages.success(request, 'fooditem added successfully')
            return redirect('menu_builder')
    else:
        form = FoodItemForm()
    context = {
        'form':form,
    }
    return render(request, 'vendors/add_fooditem.html', context)

def edit_fooditem(request, pk=None):
    fooditem = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES, instance=fooditem)
        if form.is_valid():
            form.save()
            messages.success(request, 'fooditem updated successfully')
            return redirect('menu_builder')
    else:
        form = FoodItemForm(instance=fooditem)
    context = {
        'form':form,
        'fooditem':fooditem,
    }
    return render(request, 'vendors/edit_fooditem.html', context)

def delete_fooditem(request, pk=None):
    fooditem = get_object_or_404(FoodItem, pk=pk)
    fooditem.delete()
    messages.success(request, 'fooditem has been deleted successfully')
    return redirect('menu_builder')