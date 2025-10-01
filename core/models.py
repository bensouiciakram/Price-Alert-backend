from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    def __str__(self):
        return f'{self.username}'
    

class DemoToken(models.Model):
    token = models.CharField(max_length=255)
    expire_at = models.DateTimeField()
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} token'