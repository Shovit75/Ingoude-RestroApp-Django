from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import json

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=64)
    featured = models.BooleanField(default=True)
    image = models.ImageField(upload_to='category_images/', null=True)

    def __str__(self):
        return self.name

class Food(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='foods')
    featured = models.BooleanField(default=True)
    image = models.ImageField(upload_to='food_images/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class WebUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username
    
class Chef(models.Model):
    username = models.CharField(max_length=64, unique=True)
    designation = models.CharField(max_length=128)
    featured = models.BooleanField(default=True)
    image = models.ImageField(upload_to='chef_images/', null=True)

    def __str__(self):
        return self.username
    
class Checkout(models.Model):
    username = models.CharField(max_length=64)
    address = models.TextField()
    phone = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    order = models.TextField()

    def set_order(self, order):
        self.order = json.dumps(order)

    def get_order(self):
        return json.loads(self.order)

    def __str__(self):
        return f"Order by {self.username} - Total: {self.price}"