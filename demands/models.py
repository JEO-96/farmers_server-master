from django.db import models
from products.models import Products


# Create your models here.
class Demand(models.Model):
    products_id = models.ForeignKey(Products, on_delete=models.CASCADE, unique=True) # 품종ID
    weight = models.CharField(max_length=5)  # 중량
    price = models.CharField(max_length=10)  # 가격
    limit_price = models.CharField(max_length=10)  # 중량 제한

    def __str__(self):
        return self.products_id.name, self.weight