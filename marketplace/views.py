from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from marketplace.models import Cart
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
    categories = Category.objects.filter(vendor=vendor).prefetch_related (
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

#  Function For Add_to_cart 
def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the food item exits
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                #  Check if the user has already added that item to the cart
                try:
                    checkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    #  Increase the quantity by + 1
                    checkCart.quantity += 1
                    checkCart.save()
                    return JsonResponse({'status':'Success', 'message':'Increase the cart quantity.'})
                except:
                    checkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status':'Success', 'message':'Added the food to the cart. '})
            except:
                return JsonResponse({'status':'Failed', 'message':'This Food Does not Exist.'})
        else:
            return JsonResponse({'status':'Failed', 'message':'Invalid Request!.'})
    else:
        return JsonResponse({'status':'Failed', 'message':'Please login to continue.'})
