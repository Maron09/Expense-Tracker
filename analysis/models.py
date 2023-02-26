from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User



class Expense(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    category = models.CharField(max_length=260)


    def __str__(self):
        return self.category

    class Meta:
        ordering = ['-date']


class Category(models.Model):
    name = models.CharField(max_length=260)

    class Meta:
        verbose_name_plural = 'Categories'


    def __str__(self):
        return self.name
