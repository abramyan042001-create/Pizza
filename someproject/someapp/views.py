from django.shortcuts import render, get_object_or_404
from .models import Item, Manufacturer


def index(request):
    """Главная страница"""
    # Вариант 1: Простая заглушка
    return render(request, 'index.html', {
        'title': 'Главная страница',
        'message': 'Добро пожаловать в магазин!'
    })

def item_detail(request, item_id):
    # Получаем товар по ID или возвращаем 404
    item = get_object_or_404(Item, id=item_id)
    
    # Передаем товар в контекст шаблона
    context = {
        'item': item,
        'title': f'Товар - {item.name}'
    }
    
    return render(request, '1.html', context)