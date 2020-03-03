from django.contrib import admin
from .models import Item, Unit


# Register your models here.
@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Item)
class ItemDetailAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity',)
    search_fields = ('name',)
