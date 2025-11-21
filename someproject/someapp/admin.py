from django.contrib import admin
from .models import Manufacturer, Item

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'quantity', 'manufacturer']
    list_filter = ['manufacturer']
    search_fields = ['name']