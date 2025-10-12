from django.db import models
from products.models import Product 

class Channel(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class Alert(models.Model):
    threshold = models.DecimalField(max_digits=10,decimal_places=2)
    frequency = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    channel = models.ForeignKey(Channel,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='alerts')

    def __str__(self):
        return f'{self.product.meta.title} alert'

class AlertMet(models.Model):
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name="met_events")
    triggered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert met for {self.alert.product.meta.title} at {self.triggered_at}"
