from django.db import models


# Create your models here.


class Category(models.Model):
    category = models.CharField("Category", max_length=150, blank=True, null=True)

    def __str__(self):
        return self.category


class Color(models.Model):
    color = models.CharField("Color", max_length=10, null=True, blank=True)

    def __str__(self):
        return self.color


class Brand(models.Model):
    brand = models.CharField("Brand", max_length=150)

    def __str__(self):
        return self.brand


class Product(models.Model):
    product_name = models.CharField("Product Name", max_length=150)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.CharField("Product Description", max_length=250, blank=True, null=True)
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, related_name="products", on_delete=models.CASCADE)
    color = models.ForeignKey(Color, related_name="products", on_delete=models.CASCADE)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    size = models.CharField(max_length=10, blank=True, null=True)
    type = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return f"{self.product_name}-{self.brand}"


class UploadedFile(models.Model):
    file = models.FileField(upload_to='files/')

