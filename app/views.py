from django.shortcuts import render, get_object_or_404, redirect
from vendor.models import Vendor, Category, Cart, FoodItem
from django.http import HttpResponse, JsonResponse
from app.context_processors import get_cart_count
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    context = {
        'vendors':vendors,
    }
    return render(request, 'index.html', context)

def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors':vendors,
        'vendor_count':vendor_count,
    }
    return render(request, 'marketplace/listings.html', context)

def vendor_detail(request, pk=None):
    vendor = get_object_or_404(Vendor, pk=pk)
    categories = Category.objects.filter(vendor=vendor)

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'vendor':vendor,
        'categories':categories,
        'cart_items':cart_items,
    }
    return render(request, 'marketplace/listing-detail.html', context)

def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        try:
            fooditem = FoodItem.objects.get(id=food_id)
            try:
                checkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                checkCart.quantity += 1
                checkCart.save()
                return JsonResponse({'status':'success', 'message':'Increased the cart quantity', 'cart_counter':get_cart_count(request), 'qty': checkCart.quantity})
            except:
                checkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                return JsonResponse({'status':'success', 'message':'add the food to cart', 'cart_counter':get_cart_count(request), 'qty': checkCart.quantity})
        except:
            return JsonResponse({'status':'failed', 'message':'input invalid'})
    else:
        return JsonResponse({'status':'failed', 'message':'Input invalid'})
    
def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        try:
            fooditem = FoodItem.objects.get(id=food_id)
            try:
                checkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                if checkCart.quantity > 1:
                    checkCart.quantity -= 1
                    checkCart.save()
                else:
                    checkCart.delete()
                    checkCart.quantity = 0
                return JsonResponse({'status':'success', 'message':'Increased the cart quantity', 'cart_counter':get_cart_count(request), 'qty': checkCart.quantity})
            except:
                return JsonResponse({'status':'failed', 'message':'you do not have this in your cart'})
        except:
            return JsonResponse({'status':'failed', 'message':'input invalid'})
    else:
        return JsonResponse({'status':'failed', 'message':'Input invalid'})

@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items':cart_items,
    }
    return render(request, 'marketplace/cart.html', context)

def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        try:
            cart_item = Cart.objects.get(user=request.user, id=cart_id)
            if cart_item:
                cart_item.delete()
            return JsonResponse({'status':'success', 'message':'cart has been deleted', 'cart_counter':get_cart_count(request)})
        except:
                return JsonResponse({'status':'failed', 'message':'you do not have this in your cart'})
    else:
        return JsonResponse({'status':'failed', 'message':'Input invalid'})