from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, Cart, CartItem
from django.http import JsonResponse

def cart_view(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key)

    context = {
        'cart': cart,
        'cart_items': cart.items.select_related('product'),
    }
    return render(request, 'cart.html', context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    else:
        cart_item.quantity = quantity
        cart_item.save()

    messages.success(request, f"{quantity} × {product.name} added to cart.")
    return redirect('cart')


def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    action = request.POST.get('action')

    if action == 'increase':
        item.quantity += 1
    elif action == 'decrease' and item.quantity > 1:
        item.quantity -= 1
    elif action == 'remove':
        item.delete()
        return JsonResponse({'success': True})

    item.save()
    return JsonResponse({
        'success': True,
        'quantity': item.quantity,
        'item_total': float(item.get_total_price()),
        'cart_total': float(item.cart.get_total_price()),
        'item_count': item.cart.items.count(),
    })


def clear_cart(request):
    if request.user.is_authenticated:
        Cart.objects.filter(user=request.user).delete()
    else:
        session_key = request.session.session_key
        Cart.objects.filter(session_key=session_key).delete()
    messages.info(request, "Cart cleared.")
    return redirect('cart')

def blog_page(request):
    return render(request, 'blog.html')

def about_page(request):
    return render(request, 'about.html')

def contacts_page(request):
    return render(request, 'contacts.html')
