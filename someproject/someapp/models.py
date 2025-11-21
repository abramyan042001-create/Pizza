from django.db import models

class Manufacturer(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название производителя")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"

class Item(models.Model):
    name = models.CharField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

        