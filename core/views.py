from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, Cart, CartItem
from django.http import JsonResponse
from urllib.parse import quote

# Create your views here.

def home(request):
    products = Product.objects.all()[:4]  # Get first 4 products
    context = {
        'products': products,
    }
    return render(request, 'index.html', context)


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
    # Determine which cart to use (same logic as cart_view / add_to_cart)
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            return JsonResponse({'success': False, 'error': 'No cart found'}, status=400)
        cart = Cart.objects.get(session_key=session_key)

    # Now safely get the item belonging to THAT cart
    item = get_object_or_404(CartItem, id=item_id, cart=cart)

    action = request.POST.get('action')

    if action == 'increase':
        item.quantity += 1
    elif action == 'decrease' and item.quantity > 1:
        item.quantity -= 1
    elif action == 'remove':
        item.delete()
        # After remove we can redirect or return JSON
        return JsonResponse({'success': True, 'item_count': cart.items.count()})

    item.save()

    return JsonResponse({
        'success': True,
        'quantity': item.quantity,
        'item_total': float(item.get_total_price()),
        'cart_total': float(cart.get_total_price()),
        'item_count': cart.items.count(),
    })

def clear_cart(request):
    if request.user.is_authenticated:
        Cart.objects.filter(user=request.user).delete()
    else:
        session_key = request.session.session_key
        Cart.objects.filter(session_key=session_key).delete()
    messages.info(request, "Cart cleared.")
    return redirect('cart')

def checkout_page(request):
    # Same cart logic as cart_view
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key)

    cart_items = cart.items.select_related('product')

    # If cart is empty, go back to cart
    if not cart_items.exists():
        return redirect('cart')

    # Build the WhatsApp message
    message_lines = [
        "Hello Cattleya's Coffee 👋",
        "I would like to order the following:\n"
    ]

    for item in cart_items:
        message_lines.append(
            f"• {item.quantity} × {item.product.category} - {item.product.name} — Ugx.{item.get_total_price():.2f}"
        )

    message_lines.append(f"\nTotal: Ugx. {cart.get_total_price():.2f}")
    message_lines.append("\nThank you! I'll be waiting for your confirmation.")

    full_message = "\n".join(message_lines)

    # === CHANGE THIS TO YOUR REAL WHATSAPP NUMBER ===
    YOUR_WHATSAPP_NUMBER = "+211924263348"   # ←←←←← PUT YOUR FULL NUMBER HERE (with +256)

    whatsapp_text = quote(full_message)
    whatsapp_url = f"https://wa.me/{YOUR_WHATSAPP_NUMBER.replace('+', '')}?text={whatsapp_text}"

    context = {
        'cart_items': cart_items,
        'cart_total': cart.get_total_price(),
        'whatsapp_url': whatsapp_url,
    }

    return render(request, 'checkout.html', context)


def blog_page(request):
    return render(request, 'blog.html')

def about_page(request):
    return render(request, 'about.html')

def contacts_page(request):
    return render(request, 'contacts.html')

