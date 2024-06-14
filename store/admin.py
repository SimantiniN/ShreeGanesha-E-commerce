from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display=('product_name', 'price', 'category','quantity','is_available','modified_date')
    prepopulated_fields={'product_slug': ('product_name',)}

admin.site.register(Product, ProductAdmin)