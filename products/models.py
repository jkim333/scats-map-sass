from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    unit_price = models.PositiveIntegerField()

    def __str__(self):
        return self.name
