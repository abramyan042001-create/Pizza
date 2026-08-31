from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('customer_name', 'phone', 'address', 'comment')
        widgets = {
            'customer_name': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
            'phone': forms.TextInput(attrs={'placeholder': '+7 999 000-00-00'}),
            'address': forms.TextInput(attrs={'placeholder': 'Улица, дом, квартира'}),
            'comment': forms.Textarea(attrs={'placeholder': 'Домофон, этаж или пожелания', 'rows': 3}),
        }
