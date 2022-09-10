from django.contrib import admin
from .models import *


class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    def has_delete_permission(self, request, obj=None):
        return False

class ProductsAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Categories , CategoriesAdmin)
admin.site.register(Products , ProductsAdmin)

class OrderItemInline(admin.TabularInline):
    model = OrderProducts

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline,]
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Order , OrderAdmin )
# admin.site.register(OrderProducts )