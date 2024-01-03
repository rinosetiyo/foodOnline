from django.shortcuts import render, get_object_or_404
from vendor.models import Vendor, Category

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
    context = {
        'vendor':vendor,
        'categories':categories,
    }
    return render(request, 'marketplace/listing-detail.html', context)