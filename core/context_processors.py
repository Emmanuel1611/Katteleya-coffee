from django.db.models import Sum
from .models import Cart

def cart_summary(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key)

    item_count = cart.items.count()
    total = cart.get_total_price()

    return {
        'cart_item_count': item_count,
        'cart_total': total,
        'cart': cart,
    }


def cart_count(request):
    """Adds the total number of items in the cart to every template"""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            return {'cart_count': 0}
        cart, _ = Cart.objects.get_or_create(session_key=session_key)

    # Total quantity (e.g. 3 coffees = shows "3")
    # If you prefer "number of different products", change to: cart.items.count()
    total = cart.items.aggregate(total=Sum('quantity'))['total'] or 0

    return {'cart_count': total}


