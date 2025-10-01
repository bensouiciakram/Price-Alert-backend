from django.db import models


class Website(models.Model):
    domain = models.CharField(max_length=255)


class Product(models.Model):
    url = models.URLField()
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    website = models.ManyToManyField(Website)


class Price(models.Model):
    price = models.DecimalField(max_digits=10,decimal_places=2)
    checked_at = models.DateTimeField()
    product = models.ForeignKey(Product,on_delete=models.CASCADE)


class Field(models.Model):
    field_name = models.CharField(max_length=255)


class Xpath(models.Model):
    selector = models.CharField(max_length=255)
    website = models.ForeignKey(Website,on_delete=models.CASCADE)
    field = models.ForeignKey(Field,on_delete=models.PROTECT)
    
     