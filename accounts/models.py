from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('normal', 'Normal User'),
        ('admin', 'Administrator'),
    ]
    
    ACCOUNT_STATUS_CHOICES = [
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('banned', 'Banned'),
    ]
    
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='normal')
    account_status = models.CharField(max_length=10, choices=ACCOUNT_STATUS_CHOICES, default='active')
    suspension_reason = models.TextField(blank=True, null=True)
    suspended_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='suspended_users')
    suspension_date = models.DateTimeField(null=True, blank=True)
    last_login_attempt = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.username
    
    def is_admin_user(self):
        return self.user_type == 'admin'
    
    def is_account_active(self):
        return self.account_status == 'active'
    
    def suspend_account(self, admin_user, reason="Account suspended by administrator"):
        self.account_status = 'suspended'
        self.suspension_reason = reason
        self.suspended_by = admin_user
        self.suspension_date = timezone.now()
        self.save()
    
    def reactivate_account(self):
        self.account_status = 'active'
        self.suspension_reason = None
        self.suspended_by = None
        self.suspension_date = None
        self.save()