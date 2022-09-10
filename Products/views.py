from itertools import product
from django.shortcuts import render , redirect , get_object_or_404
import time
from Products.models import Categories, Products
from .forms import *
from .cart import *

def get_category():
    v = []
    for i in Categories.objects.all():
        parent = []
        if not i.parent:
            ch1 = []
            for k in i.children.all():
                ch2 = []
                for p in k.children.all():
                    ch3 = []
                    for q in p.children.all():
                        ch4 = []
                        for r in q.children.all():
                            ch4.append({'name': r})
                        if ch4 is not []:
                            ch3.append({'name': q , 'children' : ch4})
                    if ch3 is not []:
                        ch2.append({'name':p , 'children' : ch3})
                if ch2 is not []:
                    ch1.append({'name':k,'children':ch2})
            parent.append({'name':i,'children':ch1})
            v.append(parent)
    return v

def ManageProductListView(ListView):
    products = Products.objects.all()
    context = {
        'categories' : get_category() ,
        'products' : products ,
    }
    return render(ListView , 'Product/List.html' , context)

def ManageProductDetailView(DetailView , id):
    product = get_object_or_404(Products , pk = id)
    context = {
        'categories' : get_category() ,
        'product' : product ,
    }
    return render(DetailView , 'Product/Detail.html' , context)

def ManageCategoryView(CategoryView , id = None):
    categories = Categories.objects.all()
    if id:
        products = Products.objects.all().filter(category = get_object_or_404(Categories , pk = id))
    else:
        try:
            products = Products.objects.all().filter(category = CategoryView.POST.get('category'))
        except:
            return redirect('products:listview')
    context = {
        'categories' : get_category() ,
        'products' : products ,
    }
    return render(CategoryView , 'Product/List.html' , context)

def ManageAddToCartView(AddView , id):
    cart = Cart(AddView)
    product = get_object_or_404(Products, pk=id)
    form = CartAddProductForm(AddView.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,quantity=cd['quantity'],update_quantity=cd['update'])
    time.sleep(1)
    return redirect('products:cart_detail',)

def ManageCartDetailView(DetailView):
    unorder_cart = Cart(DetailView)
    for item in unorder_cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],'update': True})
    cart = []
    for v in unorder_cart:
        quantity = (v.get('update_quantity_form'))
        t_price = (v.get('total_price'))
        price = (v.get('price'))
        product = (v.get('product'))
        cart.append({'product' : product , 'quantity' : quantity , 'price' : price , 't_price' : t_price })
    grand_total = (unorder_cart.get_total_price())
    context = {
        'cart': cart,
        'grand_total': grand_total,
    }
    return render(DetailView, 'Cart/Cart.html',context)

def ManageCartRemoveView(request, id):
    cart = Cart(request)
    product = get_object_or_404(Products, id=id)
    cart.remove(product)
    return redirect('products:cart_detail')

def ManageCheckoutView(CheckoutView):
    unorder_cart = Cart(CheckoutView)
    if CheckoutView.method == 'POST':
        form = OrderCreateForm({
            'customer' : CheckoutView.POST.get('customer') ,
            'address' : CheckoutView.POST.get('address') ,
            'contact' : CheckoutView.POST.get('contact') ,
            'total_price' : unorder_cart.get_total_price() ,
        })
        order = form.save()
        for v in unorder_cart:
            quantity = (v.get('quantity'))
            price = (v.get('price'))
            product = (v.get('product'))
            form = OrderProductsCreateForm({
                'order' : order ,
                'product' : product ,
                'qty' : quantity ,
                'unit_price' : price ,
            })
            if form.is_valid:
                form.save()
        unorder_cart.clear()
        return redirect('products:cart_detail')
    else:
        grand_total = (unorder_cart.get_total_price())
        context = {
            'grand_total': grand_total,
        }
        return render(CheckoutView , 'Cart/Checkout.html' , context)