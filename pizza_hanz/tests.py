from django.test import Client, TestCase
from django.urls import reverse

from .models import Category, Order, Pizza


class PizzaShopTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Тестовые', slug='test')
        self.pizza = Pizza.objects.create(category=self.category, name='Тест', slug='test-pizza', description='Описание', price=500, weight=500)
        self.client = Client()

    def test_menu_and_detail_open(self):
        self.assertEqual(self.client.get(reverse('menu')).status_code, 200)
        self.assertContains(self.client.get(reverse('pizza_detail', args=[self.pizza.slug])), self.pizza.name)

    def test_cart_add(self):
        response = self.client.post(reverse('cart_add', args=[self.pizza.id]))
        self.assertRedirects(response, reverse('cart'))
        self.assertEqual(self.client.session['cart'][str(self.pizza.id)], 1)

    def test_checkout_creates_order(self):
        self.client.post(reverse('cart_add', args=[self.pizza.id]))
        response = self.client.post(reverse('checkout'), {'customer_name': 'Иван', 'phone': '+79990000000', 'address': 'Улица, 1', 'comment': ''})
        order = Order.objects.get()
        self.assertRedirects(response, reverse('order_success', args=[order.id]))
        self.assertEqual(order.total, self.pizza.price)
        self.assertEqual(order.items.count(), 1)
