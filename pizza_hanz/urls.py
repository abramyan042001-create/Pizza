from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('category/<slug:category_slug>/', views.menu, name='menu_category'),
    path('pizza/<slug:slug>/', views.pizza_detail, name='pizza_detail'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:pizza_id>/', views.cart_add, name='cart_add'),
    path('cart/update/<int:pizza_id>/', views.cart_update, name='cart_update'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/<int:order_id>/success/', views.order_success, name='order_success'),
]
