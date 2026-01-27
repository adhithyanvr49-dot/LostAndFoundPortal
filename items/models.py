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
    # items/models.py
# items/models.py
from django.db import models
from django.conf import settings

class Claim(models.Model):
    # This model is required for the Claim History page
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    claimant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    proof_description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    # items/models.py
from django.db import models
from django.conf import settings

from django.db import models
from django.conf import settings # Add this import

from django.db import models
from django.conf import settings # Add this import

from django.db import models
from django.conf import settings # Required to reference the custom user model

class Message(models.Model):
    # Use settings.AUTH_USER_MODEL to fix the E301 error
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

# items/models.py
from django.db import models
from django.conf import settings

class Claim(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='claims')
    claimant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    proof_description = models.TextField(help_text="Describe details only the owner would know.")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Claim for {self.item.title} by {self.claimant.username}"