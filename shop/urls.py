# shop/urls.py
from django.urls import path
from . import views

app_name = 'shop'   # ← important for namespacing

urlpatterns = [
    path('shop/', views.shop, name='shop'),
    # path('cart/', views.cart_page, name='cart'),
    path('account/', views.account_page, name='account'),
]