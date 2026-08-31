from django.core.validators import MinValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField('Название', max_length=100, unique=True)
    slug = models.SlugField('Адрес', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Pizza(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категория', related_name='pizzas', on_delete=models.PROTECT)
    name = models.CharField('Название', max_length=150)
    slug = models.SlugField('Адрес', max_length=150, unique=True)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    weight = models.PositiveIntegerField('Вес, г', default=500)
    image_url = models.URLField('Ссылка на изображение', blank=True)
    is_available = models.BooleanField('В продаже', default=True)
    is_popular = models.BooleanField('Популярная', default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Пицца'
        verbose_name_plural = 'Пиццы'
        ordering = ('-is_popular', 'name')

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новый'),
        ('cooking', 'Готовится'),
        ('delivery', 'В доставке'),
        ('done', 'Выполнен'),
        ('cancelled', 'Отменён'),
    )

    customer_name = models.CharField('Имя', max_length=120)
    phone = models.CharField('Телефон', max_length=30)
    address = models.CharField('Адрес', max_length=250)
    comment = models.TextField('Комментарий', blank=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    total = models.DecimalField('Сумма', max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-created_at',)

    def __str__(self):
        return f'Заказ №{self.pk} — {self.customer_name}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, verbose_name='Пицца', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField('Количество', default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField('Цена', max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    @property
    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f'{self.pizza} × {self.quantity}'

# Create your models here.
