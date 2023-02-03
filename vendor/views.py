from django.shortcuts import get_object_or_404, redirect, render

from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from accounts.views import check_role_vendor
from menu.forms import CategoryForm
from menu.models import *
from vendor.models import Vendor
from .forms import VendorForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.defaultfilters import slugify

#  Helper Function For Repeated Code Get Vendor User
def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


# Create your views here.

#  Funciton For Vendor Profile...
@login_required(login_url='login') 
@user_passes_test(check_role_vendor)
def vprofile(request):
    # Fetch data
    profile = get_object_or_404(UserProfile, user= request.user)
    vendor = get_object_or_404(Vendor, user= request.user)
    # Check Form data
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request,'Settings Updated.')
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)
    
    #  pass Context for rendering data...  
    context ={
        'profile_form' : profile_form,
        'vendor_form' : vendor_form,
        'profile':profile,
        'vendor':vendor,
    }
    return render(request, 'vendor/vprofile.html', context)


#  Function For menu builder...
@login_required(login_url='login') 
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request) # get logged in User using Helper Function
    categories = Category.objects.filter(vendor=vendor)    
    context = {
        'categories':categories
    }
    return render(request, 'vendor/menu_builder.html', context)


# Function fooditems wtih category...
@login_required(login_url='login') 
@user_passes_test(check_role_vendor)
def fooditems_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category,pk=pk)
    fooditems = FoodItem.objects.filter(vendor=vendor, category=category)
    print(fooditems)
    context = {
        'fooditems':fooditems,
        'category':category
    }
    return render(request, 'vendor/fooditems_by_category.html', context)

#  Function For Add Category From UI
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request,'Category Added Successfully')
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:        
        form = CategoryForm()
    context = {
        'form':form
    }
    return render(request, 'vendor/add_category.html', context)