from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from marketplace.context_processors import get_cart_amounts, get_cart_counter
from marketplace.models import Cart
from menu.models import Category, FoodItem
from vendor.models import Vendor
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required

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
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'vendor': vendor,
        'categories' : categories,
        'cart_items' : cart_items
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
                    return JsonResponse({'status':'Success', 'message':'Increase the cart quantity.', 'cart_counter': get_cart_counter(request), 'qty': checkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    checkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status':'Success', 'message':'Added the food to the cart.', 'cart_counter': get_cart_counter(request), 'qty': checkCart.quantity, 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status':'Failed', 'message':'This Food Does not Exist.'})
        else:
            return JsonResponse({'status':'Failed', 'message':'Invalid Request!.'})
    else:
        return JsonResponse({'status':'login_required', 'message':'Please login to continue.'})


# Decrease Cart
def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the food item exits
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                #  Check if the user has already added that item to the cart
                try:
                    checkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    #  Decrease the quantity by + 1
                    if checkCart.quantity > 1:
                        checkCart.quantity -= 1
                        checkCart.save()
                    else:
                        checkCart.delete()
                        checkCart.quantity = 0
                    return JsonResponse({'status':'Success', 'cart_counter': get_cart_counter(request), 'qty': checkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    return JsonResponse({'status':'Failed', 'message':'You Do Not Have This Iteam In Cart.'})
            except:
                return JsonResponse({'status':'Failed', 'message':'This Food Does not Exist.'})
        else:
            return JsonResponse({'status':'Failed', 'message':'Invalid Request!.'})
    else:
        return JsonResponse({'status':'login_required', 'message':'Please login to continue.'})
    # return JsonResponse({'status':'Failed', 'message':'Please login to continue.'})
    

#  Function For Cart   
@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    print(cart_items)
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/cart.html',context)


#  Function For Delete The Cart Item:
def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                # Check if the cart item exists:
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status':'Success', 'message':'Cart item has been deleted', 'cart_counter': get_cart_counter(request), 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status':'Failed', 'message':'Cart item does not exist!'})
                        
        else:
            return JsonResponse({'status':'Failed', 'message':'Invalid Request!'})
        
    
# Function For Search

def search(request):
    rest_name = request.GET['rest_name']
    address = request.GET['address']
    latitude = request.GET['lat']
    longitude = request.GET['lng']
    radius = request.GET['radius']
    print(rest_name, address, latitude, longitude, radius)
    return render(request, 'marketplace/listings.html') 

        

