from multiprocessing import set_forkserver_preload
from random import choices
from secrets import choice
from statistics import mode
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

#  UserManager for Methods..
class UserManager(BaseUserManager):
    # This Class Only contains Methods not fields
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')
        
        if not username:
            raise ValueError('User must have an username')
        
        user = self.model(
            # normalize convert into small letter
            email = self.normalize_email(email), 
            username = username,
            first_name = first_name,
            last_name = last_name,
            
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password=None ):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

#  Custome User Model
class User(AbstractBaseUser):
    # This class contains DB fields
    VENDOR = 1
    CUSTOMER = 2
    
    ROLE_CHOICE = (
        (VENDOR, 'Vendor'),
        (CUSTOMER, 'Customer'),
    )
    
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    username = models.CharField(max_length = 50, unique=True)
    email = models.EmailField(max_length = 50, unique=True)
    phone_number = models.CharField(max_length = 12, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)
    
    # Required fields
    date_joined = models.DateTimeField(auto_now_add= True)
    last_login = models.DateTimeField(auto_now_add = True)
    created_date = models.DateTimeField(auto_now_add = True)
    modified_date = models.DateTimeField(auto_now_add = True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    
    # Change the login by email insted Username
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    # which class will use this User class
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    def get_role(self):
        if self.role == 1:
            user_role = 'Vendor'
        elif self.role == 2:
            user_role = 'Customer'
        return user_role
    
    
#  User Profile model  connect with Django user modal
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True, null=True)
    profile_picture = models.ImageField(upload_to = 'users/profile_pictures', blank=True, null=True)
    cover_photo = models.ImageField(upload_to = 'users/covor_photo', blank=True, null=True)
    address = models.CharField(max_length=250, blank=True,null=True)
    country = models.CharField(max_length=20, blank=True,null=True)
    province = models.CharField(max_length=50, blank=True,null=True)
    city = models.CharField(max_length=50, blank=True,null=True)
    pin_code = models.CharField(max_length=6, blank=True,null=True)
    latitude = models.CharField(max_length=20, blank=True,null=True)
    longitude = models.CharField(max_length=50, blank=True,null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    
    # def full_address(self):
    #     return f'{self.address}, {self.city}'
    
    def __str__(self):
        return self.user.email
 
 