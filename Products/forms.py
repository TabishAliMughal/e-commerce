from django import forms

from Products.models import Order, OrderProducts

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,coerce=int)
    update = forms.BooleanField(required=False,initial=False,widget=forms.HiddenInput)

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'customer',
            'address',
            'contact',
            'total_price',
        ]

class OrderProductsCreateForm(forms.ModelForm):
    class Meta:
        model = OrderProducts
        fields = [
            'order',
            'product',
            'qty',
            'unit_price',
        ]