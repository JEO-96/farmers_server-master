from django.db import models
from custom_user.models import User
from products.models import Products


# Create your models here.
class Sell(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)  # 유저ID
    products_id = models.ForeignKey(Products, on_delete=models.CASCADE)  # 품종ID
    weight = models.CharField(max_length=5)  # 판매중량
    created_at = models.DateTimeField('Created Time', auto_now_add=True, null=True)  # 등록시간

    def __str__(self):
        return self.user_id.name, self.products_id.name
