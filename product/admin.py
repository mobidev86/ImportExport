from django.contrib import admin

from product.models import Brand, Color, Category, Product, UploadedFile


# Register your models here.
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand',)


class ColorAdmin(admin.ModelAdmin):
    list_display = ('id', 'color',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'created_at', 'category', 'brand', 'color', 'size', 'price', 'type',)
    search_fields = ('product_name', 'category', 'brand')


class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file',)


admin.site.register(Brand, BrandAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(UploadedFile, UploadedFileAdmin)