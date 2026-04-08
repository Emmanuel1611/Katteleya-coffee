from django.shortcuts import render
from django.db.models import Q
from decimal import Decimal
from core.models import Product, Cart, CartItem

# Create your views here.
# shop/views.py
from django.shortcuts import render

def shop_page(request):
    query = request.GET.get('q', '').strip()
    min_price_str = request.GET.get('min_price')
    max_price_str = request.GET.get('max_price')
    products = Product.objects.filter(is_available=True)
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if min_price_str:
        products = products.filter(price__gte=Decimal(min_price_str))
    if max_price_str:
        products = products.filter(price__lte=Decimal(max_price_str))
    products = products.order_by('-created')
    context = {
        'products': products, 
        'query': query,
        'min_price': min_price_str or '',
        'max_price': max_price_str or ''
    }
    if request.GET.get('partial') == 'true':
        return render(request, 'shop/_products_partial.html', context)
    return render(request, 'shop.html', context)


def shop(request):
    query = request.GET.get('q', '').strip()
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    selected_category = request.GET.get('category')

    products = Product.objects.filter(is_available=True)

    # ✅ SEARCH (name + category string)
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(category__icontains=query)
        )

    # ✅ CATEGORY FILTER (string match)
    if selected_category:
        products = products.filter(category=selected_category)

    # ✅ PRICE FILTER
    if min_price:
        products = products.filter(price__gte=Decimal(min_price))
    if max_price:
        products = products.filter(price__lte=Decimal(max_price))

    products = products.order_by('-created')

    # ✅ GET UNIQUE CATEGORY STRINGS
    categories = Product.objects.values_list('category', flat=True).distinct()

    context = {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': selected_category,
        'min_price': min_price or '',
        'max_price': max_price or '',
    }

    if request.GET.get('partial'):
        return render(request, 'shop/_products_partial.html', context)

    return render(request, 'shop.html', context)

def cart_page(request):
    return render(request, 'shop/cart.html')

from urllib.parse import quote
from django.shortcuts import render, redirect


def account_page(request):
    return render(request, 'account.html')