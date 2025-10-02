from django.db import models


class Website(models.Model):
    domain = models.CharField(max_length=255)


class ProductMetaData(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/')

class Product(models.Model):
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    website = models.ManyToManyField(Website)
    meta = models.OneToOneField(ProductMetaData,on_delete=models.CASCADE)


class PriceHistory(models.Model):
    price = models.DecimalField(max_digits=10,decimal_places=2)
    checked_at = models.DateTimeField()
    product = models.ForeignKey(Product,on_delete=models.CASCADE)


class Xpath(models.Model):
    website = models.ForeignKey(Website,on_delete=models.CASCADE)
    price_selector = models.CharField(max_length=255,null=True)
    image_selector = models.CharField(max_length=255,null=True)
    title_selector = models.CharField(max_length=255,null=True)
    
     