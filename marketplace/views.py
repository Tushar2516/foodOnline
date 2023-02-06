from django.shortcuts import get_object_or_404, render
from menu.models import Category, FoodItem
from vendor.models import Vendor
from django.db.models import Prefetch

# Create your views here.
# Function For Marketplace, Showing Registerd Hotels.
def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendors_count =vendors.count()
    context = {
        'vendors': vendors,
        'vendors_count':vendors_count,
    }
    return render(request, 'marketplace/listings.html', context)

# Function For Vendor Details
def vendor_detail(request, vendor_slug): 
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        # Here Prefetch Used For Fetch Data From FoodItems Table Using Reverse Look Up using category table.
        Prefetch(
            'fooditems',
            queryset=FoodItem.objects.filter(is_available=True)
        )
        
    )
    
    
    #  Pass Vendor Info Dict* To Vendor Details Page...
    context = {
        'vendor':vendor,
        'categories' :categories
    }
    return render(request, 'marketplace/vendor_detail.html', context)