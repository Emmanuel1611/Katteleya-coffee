# shop/urls.py
from django.urls import path
from . import views

app_name = 'shop'   # ← important for namespacing

urlpatterns = [
    path('shop/', views.shop_page, name='shop'),
    path('cart/', views.cart_page, name='cart'),
    path('checkout/', views.checkout_page, name='checkout'),
    path('account/', views.account_page, name='account'),
]