from . import views
from django.urls import path, include 

urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    
    path('<slug:vendor_slug>/', views.vendor_detail, name='vendor_detail'),
    
    # Add To Cart
    path('add_to_cart/<int:food_id>', views.add_to_cart, name='add_to_cart'),
    # Decrease Car
    path('decrease_cart/<int:food_id>/', views.decrease_cart, name = 'decrease_cart'),
    # Delete cart item
    path('delete_cart/<int:cart_id>/', views.delete_cart, name='delete_cart'), 

] 