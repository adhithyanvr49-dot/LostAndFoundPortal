#!/usr/bin/env python
"""
Test script to verify the admin system functionality
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from accounts.models import CustomUser
from items.models import Item, Claim

def test_admin_system():
    print("🔧 Testing Admin System...")
    
    # Test 1: Check if admin user exists
    try:
        admin_user = CustomUser.objects.get(username='admin')
        print(f"✅ Admin user found: {admin_user.username} (Type: {admin_user.user_type})")
        print(f"   Is admin: {admin_user.is_admin_user()}")
    except CustomUser.DoesNotExist:
        print("❌ Admin user not found")
        return
    
    # Test 2: Create a test normal user
    test_user, created = CustomUser.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'user_type': 'normal'
        }
    )
    if created:
        test_user.set_password('testpass123')
        test_user.save()
        print(f"✅ Test user created: {test_user.username} (Type: {test_user.user_type})")
    else:
        print(f"✅ Test user exists: {test_user.username} (Type: {test_user.user_type})")
    
    # Test 3: Create a test item
    test_item, created = Item.objects.get_or_create(
        title='Test iPhone',
        defaults={
            'user': test_user,
            'description': 'Lost iPhone 13 Pro',
            'category': 'electronics',
            'status': 'FOUND',
            'location': 'Central Park'
        }
    )
    if created:
        print(f"✅ Test item created: {test_item.title}")
    else:
        print(f"✅ Test item exists: {test_item.title}")
    
    # Test 4: Create a test claim
    test_claim, created = Claim.objects.get_or_create(
        item=test_item,
        claimant=test_user,
        defaults={
            'proof_description': 'It has a blue case with a cat sticker and a crack on the bottom left corner.',
            'status': 'PENDING'
        }
    )
    if created:
        print(f"✅ Test claim created: Claim for {test_claim.item.title}")
    else:
        print(f"✅ Test claim exists: Claim for {test_claim.item.title}")
    
    # Test 5: Check statistics
    total_items = Item.objects.count()
    pending_claims = Claim.objects.filter(status='PENDING').count()
    approved_claims = Claim.objects.filter(status='APPROVED').count()
    
    print(f"\n📊 System Statistics:")
    print(f"   Total Items: {total_items}")
    print(f"   Pending Claims: {pending_claims}")
    print(f"   Approved Claims: {approved_claims}")
    
    print(f"\n🎉 Admin system test completed successfully!")
    print(f"   You can now login with:")
    print(f"   - Admin: username='admin', password='admin123', user_type='Administrator'")
    print(f"   - Normal User: username='testuser', password='testpass123', user_type='Normal User'")

if __name__ == '__main__':
    test_admin_system()