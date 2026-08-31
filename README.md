# Pizza House

Учебный сайт пиццерии на Django 5.2.

## Возможности

- каталог и фильтрация пицц по категориям;
- отдельная страница товара;
- корзина на основе сессии;
- оформление заказа;
- управление меню и заказами через Django Admin;
- адаптивный дизайн;
- демонстрационные данные загружаются миграцией.

## Запуск

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Сайт: http://127.0.0.1:8000/

Админка: http://127.0.0.1:8000/admin/

После `migrate` в меню автоматически появятся демонстрационные пиццы.

Для публикации задайте переменные `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False` и
`DJANGO_ALLOWED_HOSTS=ваш-домен.ru`.
