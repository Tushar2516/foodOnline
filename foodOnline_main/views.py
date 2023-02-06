from django.shortcuts import render
from django.http import HttpResponse

from vendor.models import Vendor

#  Function For Home Page. 
def home(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8] # Limit 8 Restaurants For Home Page...
    
    # Pass The Vendor Result Dict* To Home Page
    context = {
        'vendors' : vendors,
    }
    return render(request,'home.html', context)
