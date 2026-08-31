from decimal import Decimal

from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import OrderForm
from .models import Category, OrderItem, Pizza


def _cart_data(request):
    cart = request.session.get('cart', {})
    pizzas = Pizza.objects.filter(id__in=cart.keys(), is_available=True).select_related('category')
    items, total, count = [], Decimal('0'), 0
    for pizza in pizzas:
        quantity = max(1, int(cart.get(str(pizza.id), 1)))
        subtotal = pizza.price * quantity
        items.append({'pizza': pizza, 'quantity': quantity, 'subtotal': subtotal})
        total += subtotal
        count += quantity
    return items, total, count


def menu(request, category_slug=None):
    categories = Category.objects.all()
    pizzas = Pizza.objects.filter(is_available=True).select_related('category')
    selected = None
    if category_slug:
        selected = get_object_or_404(Category, slug=category_slug)
        pizzas = pizzas.filter(category=selected)
    _, _, cart_count = _cart_data(request)
    return render(request, 'pizza_hanz/menu.html', {'categories': categories, 'pizzas': pizzas, 'selected_category': selected, 'cart_count': cart_count})


def pizza_detail(request, slug):
    pizza = get_object_or_404(Pizza.objects.select_related('category'), slug=slug, is_available=True)
    _, _, cart_count = _cart_data(request)
    return render(request, 'pizza_hanz/detail.html', {'pizza': pizza, 'cart_count': cart_count})


@require_POST
def cart_add(request, pizza_id):
    get_object_or_404(Pizza, id=pizza_id, is_available=True)
    cart = request.session.get('cart', {})
    key = str(pizza_id)
    cart[key] = min(int(cart.get(key, 0)) + 1, 20)
    request.session['cart'] = cart
    messages.success(request, 'Пицца добавлена в корзину')
    return redirect(request.POST.get('next') or 'cart')


@require_POST
def cart_update(request, pizza_id):
    cart = request.session.get('cart', {})
    try:
        quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        return HttpResponseBadRequest('Некорректное количество')
    key = str(pizza_id)
    if quantity <= 0:
        cart.pop(key, None)
    else:
        cart[key] = min(quantity, 20)
    request.session['cart'] = cart
    return redirect('cart')


def cart(request):
    items, total, count = _cart_data(request)
    return render(request, 'pizza_hanz/cart.html', {'items': items, 'total': total, 'cart_count': count})


@transaction.atomic
def checkout(request):
    items, total, count = _cart_data(request)
    if not items:
        messages.warning(request, 'Сначала добавьте пиццу в корзину')
        return redirect('menu')
    form = OrderForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        order = form.save(commit=False)
        order.total = total
        order.save()
        OrderItem.objects.bulk_create([OrderItem(order=order, pizza=item['pizza'], quantity=item['quantity'], price=item['pizza'].price) for item in items])
        request.session['cart'] = {}
        return redirect('order_success', order_id=order.id)
    return render(request, 'pizza_hanz/checkout.html', {'form': form, 'items': items, 'total': total, 'cart_count': count})


def order_success(request, order_id):
    return render(request, 'pizza_hanz/success.html', {'order_id': order_id, 'cart_count': 0})
