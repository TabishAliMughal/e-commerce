from django.contrib import admin
from .models import *

admin.site.register(Categories)
admin.site.register(Products)

class OrderItemInline(admin.TabularInline):
    model = OrderProducts

class OrderAdmin(admin.ModelAdmin):
   inlines = [OrderItemInline,]


admin.site.register(Order , OrderAdmin )
# admin.site.register(OrderProducts )