from django.db import migrations


def add_demo_data(apps, schema_editor):
    Category = apps.get_model('pizza_hanz', 'Category')
    Pizza = apps.get_model('pizza_hanz', 'Pizza')
    classic = Category.objects.create(name='Классические', slug='classic')
    meat = Category.objects.create(name='Мясные', slug='meat')
    veggie = Category.objects.create(name='Вегетарианские', slug='veggie')
    rows = [
        (classic, 'Маргарита', 'margarita', 'Томаты, моцарелла, фирменный томатный соус и свежий базилик.', 499, 480, True),
        (classic, 'Пепперони', 'pepperoni', 'Пикантная пепперони, много моцареллы и томатный соус.', 599, 520, True),
        (meat, 'Мясной пир', 'meat-feast', 'Ветчина, бекон, пепперони, курица и моцарелла.', 749, 600, True),
        (meat, 'Барбекю', 'bbq', 'Курица, бекон, красный лук, моцарелла и соус барбекю.', 689, 570, False),
        (veggie, 'Четыре сыра', 'four-cheese', 'Моцарелла, чеддер, пармезан и сыр с голубой плесенью.', 699, 500, False),
        (veggie, 'Овощная', 'vegetable', 'Томаты, сладкий перец, шампиньоны, маслины и моцарелла.', 559, 510, False),
    ]
    for category, name, slug, description, price, weight, popular in rows:
        Pizza.objects.create(category=category, name=name, slug=slug, description=description, price=price, weight=weight, is_popular=popular)


class Migration(migrations.Migration):
    dependencies = [('pizza_hanz', '0001_initial')]
    operations = [migrations.RunPython(add_demo_data, migrations.RunPython.noop)]
