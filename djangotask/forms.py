from django import forms
from .models import Item,Unit

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'description', 'quantity','unit',)
