from django.contrib import admin
from models import Cart, Item

class CartAdmin(admin.ModelAdmin):
	list_display = ('id', 'creation_date', 'checked_out','user')
	list_filter = ('checked_out',)
	
class ItemAdmin(admin.ModelAdmin):
	list_display = ('id', 'cart', 'quantity', 'unit_price', 'object_id',)
	
admin.site.register(Cart, CartAdmin)
admin.site.register(Item, ItemAdmin)
