from django.contrib import admin

from .models import Category, Order, OrderItem, Pizza


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'weight', 'is_available', 'is_popular')
    list_filter = ('category', 'is_available', 'is_popular')
    list_editable = ('price', 'is_available', 'is_popular')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('pizza', 'quantity', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'phone', 'total', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    list_editable = ('status',)
    search_fields = ('customer_name', 'phone', 'address')
    inlines = (OrderItemInline,)

# Register your models here.
