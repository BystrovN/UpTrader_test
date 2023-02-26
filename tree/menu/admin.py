from django.contrib import admin

from .models import Item, Category


class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'category')
    list_filter = ('category',)


admin.site.register(Item, ItemAdmin)
admin.site.register(Category)
