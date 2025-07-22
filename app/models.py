from django.db import models


class Expense(models.Model):
    description = models.CharField(max_length=255)
    amount = models.FloatField()
    category = models.CharField(max_length=100)
    date = models.DateField()
    json_id = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return f"{self.description} - {self.amount} ({self.category})"
