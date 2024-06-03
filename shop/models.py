from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tailor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()

class Dress(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tailor = models.ForeignKey(Tailor, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='dresses/')

class Measurement(models.Model):
    bust = models.JSONField()
    waist = models.JSONField(default=dict)
    height = models.JSONField(default=dict)
    hips = models.JSONField(default=dict)
    submitted_at = models.DateTimeField(auto_now_add=True)
    dress = models.ForeignKey(Dress, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class database(models.Model):
    backup = models.CharField(default=0, max_length=100)
    restore = models.CharField(default=0, max_length=100)



