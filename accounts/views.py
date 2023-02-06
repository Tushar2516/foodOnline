from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render, HttpResponse, redirect
from accounts.utils import *

from vendor.forms import VendorForm
from vendor.models import Vendor
from .forms import *
from django.contrib import messages, auth
from .models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.template.defaultfilters import slugify

#  Cusotme Decorators for restrict vendor to access customer acc
#  Cusotme Decorators for restrict customer to access vendor acc

#  Check the user is vendor
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied
#  check the user is customer
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied
    

# Create your views here.

#  Function for User Registration.
def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in')
        return redirect('myAccount')
    elif request.method == 'POST':
        
        form = UserForm(request.POST)
        if form.is_valid():
            # Create the user using the form
            # Password hashing 
            # password = form.cleaned_data['password']
            # #  store data in user before saving
            # user = form.save(commit = False)
            # user.set_password(password)
            # #  Giving role
            # user.role = User.CUSTOMER
            # user.save()
            
            #  Create the user using create_user method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role = User.CUSTOMER
            user.save()
            
            #  Send Verification email
            mail_subject = 'Please Activate Your Account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            
            messages.success(request, 'Your account has been registerd successfully..')
            return redirect('registerUser')
        else:
            print('Invalid form')
            print(form.errors)
    else:
        form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/registerUser.html', context)



#  Function for Vendor Registration..
def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in')
        return redirect('myAccount')
    elif request.method == 'POST':
    #   Store the data and create the user
        form = UserForm(request.POST)  # Common Field taken from User Form
        v_form = VendorForm(request.POST, request.FILES)  # When we take Images Need to write 'request.FILES'
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            vendor_name = v_form.cleaned_data['vendor_name']
            vendor.vendor_slug = slugify(vendor_name)+'-'+str(user.id)
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            
              #  Send Verification email
            mail_subject = 'Please Activate Your Account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            
            messages.success(request, 'Your vendor account has been registered successfully.. Please wait for approval from the Admin side..')
            return redirect('registerVendor')
        else:
            print('The vendor form is Invalid')
            print(form.errors)
    
    else:
        form = UserForm()
        v_form = VendorForm()
    
    context = {
        'form' : form,
        'v_form': v_form,
    }
    
    return render(request, 'accounts/registerVendor.html', context)


#  Activate user by decode the code
def activate(request, uidb64, token):
    # Activate user by setting is_activate is True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulation! Your account is activated.')
        return redirect('myAccount')
    else:  
        messages.error(request, 'Invalid activation link')
        return redirect('myAccount')
    
#  Function For Login.
def login(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in')
        return redirect('myAccount')
    if request.method == 'POST':
        email = request.POST['email']  # fetching email and password form login page
        password = request.POST['password']
        print(email)
        print(password)        
        #  inbuilt function for login check
        user = auth.authenticate(email=email, password=password)
        print(user)
        if user is not None:
            auth.login(request, user)
            messages.success(request,' You are logged in..')
            return redirect('myAccount')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')

#  Function For Logout.
def logout(request):
    auth.logout(request)
    messages.info(request,'You are Logged Out..')
    return redirect('login')


@login_required(login_url='login')  # login required decoraters
#  Function For MyAccount.
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

# Specific Dashboard for Customer
@login_required(login_url='login') 
@user_passes_test(check_role_customer)
def customerDashboard(request):
    return render(request, 'accounts/customerDashboard.html')

# Specific Dashboard for Vendor
@login_required(login_url='login') 
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')


#  Function For Forgot Password.
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']        
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            
            # send reset password email
            mail_subject = 'Reset Your Password'
            email_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, 'Password reset link has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist.')
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')

#  Function For Reset Password Validate.
def reset_password_validate(request, uidb64, token):
    #  validate the user by decoding the token and user PK
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please Reset Your Password')
        return redirect('reset_password')
    else:
        messages.error(request,'This link has been expired!')
        return redirect('myAccount')

#  Function For Reset Passsword
def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_Active = True
            user.save()
            messages.success(request, 'Password Rest Successfully')
            return redirect('login')
        else:
            messages.error(request,' Passwords Do Not Matchs Both Should Be Same.')
            return redirect('reset_password')
    return render(request, 'accounts/reset_password.html')

