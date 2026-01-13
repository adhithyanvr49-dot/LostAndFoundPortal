# items/models.py
from django.db import models
from django.conf import settings

class Item(models.Model):
    # Define your categories here
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics (Phones, Laptops)'),
        ('documents', 'Documents (ID, Passport, Wallet)'),
        ('pets', 'Pets & Animals'),
        ('accessories', 'Accessories (Keys, Glasses, Bags)'),
        ('others', 'Others'),
    ]

    STATUS_CHOICES = [
        ('LOST', 'Lost'),
        ('FOUND', 'Found'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    # Change category to use choices
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=5, choices=STATUS_CHOICES)
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title