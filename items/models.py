from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField()
    category = models.ForeignKey(
        Category, related_name="subcategories", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    # category = models.ForeignKey(
    #     Category, related_name="products", on_delete=models.CASCADE
    # )
    sub_category = models.ForeignKey(
        SubCategory, related_name="products", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name