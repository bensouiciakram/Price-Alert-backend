from django.db import models


class Website(models.Model):
    url = models.CharField(max_length=255)
    scraping_method = models.CharField(max_length=255)

    def __str__(self):
        return self.url


class ProductMetaData(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f'{self.title} metadata'


class Product(models.Model):
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    website = models.ForeignKey(Website,on_delete=models.CASCADE)
    meta = models.OneToOneField(ProductMetaData,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.meta.title}'

class PriceHistory(models.Model):
    price = models.DecimalField(max_digits=10,decimal_places=2)
    checked_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.checked_at} price'

class Xpath(models.Model):
    website = models.ForeignKey(Website,on_delete=models.CASCADE)
    price_selector = models.CharField(max_length=255,null=True)
    image_selector = models.CharField(max_length=255,null=True)
    title_selector = models.CharField(max_length=255,null=True)
    price_cleanup = models.CharField(max_length=255,null=True)
    title_cleanup = models.CharField(max_length=255,null=True)
    image_cleanup = models.CharField(max_length=255,null=True)
    
    def __str__(self):
        return f'{self.website} xpath'
     
        