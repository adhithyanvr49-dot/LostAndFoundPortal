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
    CLAIM_TYPE_CHOICES = [
        ('ownership', 'Ownership Claim'),
        ('found_my_item', 'Found My Lost Item'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('UNDER_REVIEW', 'Under Review'),
    ]
    
    item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='claims')
    claimant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    claim_type = models.CharField(max_length=20, choices=CLAIM_TYPE_CHOICES, default='ownership')
    proof_description = models.TextField(help_text="Describe details only the owner would know.")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_claims')
    verification_date = models.DateTimeField(null=True, blank=True)
    verification_notes = models.TextField(blank=True, null=True, help_text="Admin notes about the verification")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_claim_type_display()} for {self.item.title} by {self.claimant.username}"
    
    def is_own_item_claim(self):
        """Check if user is claiming their own reported item"""
        return self.claimant == self.item.user and self.claim_type == 'found_my_item'