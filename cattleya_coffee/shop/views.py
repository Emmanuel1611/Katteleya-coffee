from django.shortcuts import render
from django.db.models import Q
from decimal import Decimal
from core.models import Product

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

def cart_page(request):
    return render(request, 'shop/cart.html')

def checkout_page(request):
    return render(request, 'checkout.html')

def account_page(request):
    return render(request, 'account.html')