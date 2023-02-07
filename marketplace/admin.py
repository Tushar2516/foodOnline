from django.contrib import admin
from .models import *


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'fooditem', 'quantity', 'created_at', 'updated_at')

# Register your models here.
admin.site.register(Cart, CartAdmin)