from django.db import models

# Create your models here.


class Product(models.Model):
    name=models.CharField(max_length=100)
    price=models.FloatField()
    description=models.TextField()
    image=models.ImageField(upload_to='images/')
    slug=models.SlugField(max_length=100)
    stock=models.IntegerField()
    active=models.BooleanField()
