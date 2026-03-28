from django.shortcuts import render
from core.models import Product

# Create your views here.
# shop/views.py
from django.shortcuts import render

def shop_page(request):
    products = Product.objects.filter(is_available=True).order_by('-created')[:6]
    return render(request, 'shop.html', {'products': products})

def cart_page(request):
    return render(request, 'shop/cart.html')

def checkout_page(request):
    return render(request, 'checkout.html')

def account_page(request):
    return render(request, 'account.html')