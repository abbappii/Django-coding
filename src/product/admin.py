from django.contrib import admin

# Register your models here.
from .models import Product, ProductImage,ProductVariant,ProductVariantPrice,Variant

class Padmin(admin.ModelAdmin):
    list_display = ['id','created_at']
admin.site.register(Product,Padmin)

admin.site.register(ProductImage)
admin.site.register(ProductVariant)
admin.site.register(ProductVariantPrice)

admin.site.register(Variant) 