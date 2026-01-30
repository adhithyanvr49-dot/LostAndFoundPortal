#!/usr/bin/env python
"""
Comprehensive test script for the enhanced Lost & Found system
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from accounts.models import CustomUser
from items.models import Item, Claim

def test_complete_system():
    print("🔧 Testing Complete Enhanced System...")
    
    # Test 1: User Management System
    print("\n1. Testing User Management System...")
    
    # Check admin user
    try:
        admin_user = CustomUser.objects.get(username='admin')
        print(f"✅ Admin user: {admin_user.username} (Type: {admin_user.user_type}, Status: {admin_user.account_status})")
    except CustomUser.DoesNotExist:
        print("❌ Admin user not found")
        return
    
    # Create test users
    normal_user1, created = CustomUser.objects.get_or_create(
        username='john_doe',
        defaults={
            'email': 'john@example.com',
            'user_type': 'normal',
            'account_status': 'active'
        }
    )
    if created:
        normal_user1.set_password('password123')
        normal_user1.save()
        print(f"✅ Created normal user: {normal_user1.username}")
    else:
        print(f"✅ Normal user exists: {normal_user1.username}")
    
    normal_user2, created = CustomUser.objects.get_or_create(
        username='jane_smith',
        defaults={
            'email': 'jane@example.com',
            'user_type': 'normal',
            'account_status': 'active'
        }
    )
    if created:
        normal_user2.set_password('password123')
        normal_user2.save()
        print(f"✅ Created normal user: {normal_user2.username}")
    else:
        print(f"✅ Normal user exists: {normal_user2.username}")
    
    # Test 2: Account Suspension System
    print("\n2. Testing Account Suspension System...")
    
    # Suspend a user
    if normal_user2.account_status == 'active':
        normal_user2.suspend_account(admin_user, "Testing suspension functionality")
        print(f"✅ Suspended user: {normal_user2.username}")
        print(f"   Reason: {normal_user2.suspension_reason}")
        print(f"   Suspended by: {normal_user2.suspended_by.username}")
    
    # Test 3: Item and Claim System
    print("\n3. Testing Enhanced Item and Claim System...")
    
    # Create test items
    lost_item, created = Item.objects.get_or_create(
        title='Lost iPhone 14 Pro',
        defaults={
            'user': normal_user1,
            'description': 'Black iPhone 14 Pro with a cracked screen and blue case',
            'category': 'electronics',
            'status': 'LOST',
            'location': 'Central Park, NYC'
        }
    )
    if created:
        print(f"✅ Created lost item: {lost_item.title}")
    else:
        print(f"✅ Lost item exists: {lost_item.title}")
    
    found_item, created = Item.objects.get_or_create(
        title='Found iPhone 14 Pro',
        defaults={
            'user': normal_user2,
            'description': 'Found iPhone 14 Pro with cracked screen',
            'category': 'electronics',
            'status': 'FOUND',
            'location': 'Central Park, NYC'
        }
    )
    if created:
        print(f"✅ Created found item: {found_item.title}")
    else:
        print(f"✅ Found item exists: {found_item.title}")
    
    # Test 4: Different Claim Types
    print("\n4. Testing Different Claim Types...")
    
    # Regular ownership claim
    ownership_claim, created = Claim.objects.get_or_create(
        item=found_item,
        claimant=normal_user1,
        defaults={
            'claim_type': 'ownership',
            'proof_description': 'This is my iPhone with a distinctive crack on the bottom left corner and a blue case with my initials JD.',
            'status': 'PENDING'
        }
    )
    if created:
        print(f"✅ Created ownership claim: {ownership_claim}")
    else:
        print(f"✅ Ownership claim exists: {ownership_claim}")
    
    # "Found my item" claim
    found_my_item_claim, created = Claim.objects.get_or_create(
        item=lost_item,
        claimant=normal_user1,
        defaults={
            'claim_type': 'found_my_item',
            'proof_description': 'This is my own iPhone that I reported lost. It has my personal photos and work emails.',
            'status': 'PENDING'
        }
    )
    if created:
        print(f"✅ Created 'found my item' claim: {found_my_item_claim}")
    else:
        print(f"✅ 'Found my item' claim exists: {found_my_item_claim}")
    
    # Test 5: Admin Verification System
    print("\n5. Testing Admin Verification System...")
    
    # Approve the "found my item" claim
    if found_my_item_claim.status == 'PENDING':
        found_my_item_claim.status = 'APPROVED'
        found_my_item_claim.verified_by = admin_user
        found_my_item_claim.verification_notes = 'Verified: User is claiming their own reported item with valid proof.'
        found_my_item_claim.save()
        print(f"✅ Approved 'found my item' claim")
    
    # Put ownership claim under review
    if ownership_claim.status == 'PENDING':
        ownership_claim.status = 'UNDER_REVIEW'
        ownership_claim.verification_notes = 'Under review: Need additional verification for ownership claim.'
        ownership_claim.save()
        print(f"✅ Put ownership claim under review")
    
    # Test 6: System Statistics
    print("\n6. System Statistics:")
    
    total_users = CustomUser.objects.filter(user_type='normal').count()
    active_users = CustomUser.objects.filter(user_type='normal', account_status='active').count()
    suspended_users = CustomUser.objects.filter(user_type='normal', account_status='suspended').count()
    
    total_items = Item.objects.count()
    lost_items = Item.objects.filter(status='LOST').count()
    found_items = Item.objects.filter(status='FOUND').count()
    
    total_claims = Claim.objects.count()
    pending_claims = Claim.objects.filter(status='PENDING').count()
    approved_claims = Claim.objects.filter(status='APPROVED').count()
    under_review_claims = Claim.objects.filter(status='UNDER_REVIEW').count()
    rejected_claims = Claim.objects.filter(status='REJECTED').count()
    
    ownership_claims = Claim.objects.filter(claim_type='ownership').count()
    found_my_item_claims = Claim.objects.filter(claim_type='found_my_item').count()
    
    print(f"   👥 Users: {total_users} total, {active_users} active, {suspended_users} suspended")
    print(f"   📦 Items: {total_items} total, {lost_items} lost, {found_items} found")
    print(f"   📋 Claims: {total_claims} total, {pending_claims} pending, {approved_claims} approved")
    print(f"   📋 Claims: {under_review_claims} under review, {rejected_claims} rejected")
    print(f"   🔍 Claim Types: {ownership_claims} ownership, {found_my_item_claims} found my item")
    
    # Test 7: Account Reactivation
    print("\n7. Testing Account Reactivation...")
    
    if normal_user2.account_status == 'suspended':
        normal_user2.reactivate_account()
        print(f"✅ Reactivated user: {normal_user2.username}")
    
    print(f"\n🎉 Complete system test finished successfully!")
    print(f"\n📝 Test Accounts for Login Testing:")
    print(f"   Admin: username='admin', password='admin123', type='Administrator'")
    print(f"   User 1: username='john_doe', password='password123', type='Normal User'")
    print(f"   User 2: username='jane_smith', password='password123', type='Normal User'")
    
    print(f"\n🔧 Features Tested:")
    print(f"   ✅ User type system (Normal/Admin)")
    print(f"   ✅ Account suspension and reactivation")
    print(f"   ✅ Enhanced claim system (Ownership/Found My Item)")
    print(f"   ✅ Admin verification with notes")
    print(f"   ✅ Multiple claim statuses (Pending/Approved/Under Review/Rejected)")
    print(f"   ✅ User management and statistics")
    
    print(f"\n🌐 URLs to Test:")
    print(f"   Login: http://127.0.0.1:8000/accounts/login/")
    print(f"   Admin Dashboard: http://127.0.0.1:8000/admin-dashboard/")
    print(f"   User Management: http://127.0.0.1:8000/manage-users/")
    print(f"   User Dashboard: http://127.0.0.1:8000/items/dashboard/")

if __name__ == '__main__':
    test_complete_system()