from django.urls import path

from .views import *

app_name = 'Products'

urlpatterns = [
    path('' , ManageProductListView , name="listview" ),
    path('product/<id>' , ManageProductDetailView , name="detailview" ),
    path('category/' , ManageCategoryView , name="category" ),
    path('category/<id>' , ManageCategoryView , name="category" ),
    path('cart/<id>' , ManageAddToCartView , name="cart_add" ),
    path('my-cart/' , ManageCartDetailView , name="cart_detail" ),
    path('my-cart/remove/<id>' , ManageCartRemoveView , name="cart_remove" ),
    path('my-cart/checkout' , ManageCheckoutView , name="cart_checkout" ),
]