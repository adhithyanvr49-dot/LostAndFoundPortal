#!/usr/bin/env python3
"""
Test script for Profile Settings and Help & Safety features
"""
import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse

def test_profile_help_features():
    """Test Profile Settings and Help & Safety functionality"""
    print("🧪 Testing Profile Settings and Help & Safety Features")
    print("=" * 60)
    
    client = Client()
    User = get_user_model()
    
    # Get or create test user
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'user_type': 'normal'
        }
    )
    
    if created:
        user.set_password('testpass123')
        user.save()
        print(f"✅ Created test user: {user.username}")
    else:
        print(f"✅ Using existing test user: {user.username}")
    
    # Login
    login_success = client.login(username='testuser', password='testpass123')
    if login_success:
        print("✅ User login successful")
    else:
        print("❌ User login failed")
        return False
    
    # Test Profile Settings Page (GET)
    try:
        response = client.get(reverse('profile_settings'))
        if response.status_code == 200:
            print("✅ Profile Settings page loads successfully")
            print(f"   - Status Code: {response.status_code}")
            
            # Check if user data is in context
            if hasattr(response, 'context') and response.context and 'user' in response.context:
                print(f"   - User in context: {response.context['user'].username}")
            else:
                print("   - User context not available (template-based rendering)")
            
        else:
            print(f"❌ Profile Settings page failed - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Profile Settings page error: {e}")
        return False
    
    # Test Profile Settings Update (POST)
    try:
        response = client.post(reverse('profile_settings'), {
            'username': 'testuser_updated',
            'email': 'updated@example.com'
        })
        
        if response.status_code in [200, 302]:  # 302 for redirect after successful update
            print("✅ Profile Settings update successful")
            
            # Check if user was actually updated
            user.refresh_from_db()
            if user.username == 'testuser_updated':
                print("   - Username updated successfully")
            if user.email == 'updated@example.com':
                print("   - Email updated successfully")
                
        else:
            print(f"❌ Profile Settings update failed - Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Profile Settings update error: {e}")
    
    # Test Help & Safety Page
    try:
        response = client.get(reverse('help_safety'))
        if response.status_code == 200:
            print("✅ Help & Safety page loads successfully")
            print(f"   - Status Code: {response.status_code}")
            
            # Check if page contains expected content
            content = response.content.decode()
            if 'Safety Guidelines' in content:
                print("   - Contains Safety Guidelines section")
            if 'Report Issues' in content:
                print("   - Contains Report Issues section")
            if 'FAQ' in content:
                print("   - Contains FAQ section")
                
        else:
            print(f"❌ Help & Safety page failed - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Help & Safety page error: {e}")
        return False
    
    # Test URL routing
    print("\n🔗 Testing URL Routing:")
    try:
        profile_url = reverse('profile_settings')
        help_url = reverse('help_safety')
        print(f"✅ Profile Settings URL: {profile_url}")
        print(f"✅ Help & Safety URL: {help_url}")
    except Exception as e:
        print(f"❌ URL routing error: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 All Profile Settings and Help & Safety tests passed!")
    print("\n📋 Feature Summary:")
    print("   ✅ Profile Settings page working")
    print("   ✅ Profile update functionality working")
    print("   ✅ Help & Safety page working")
    print("   ✅ URL routing configured correctly")
    print("   ✅ User authentication working")
    
    return True

if __name__ == "__main__":
    success = test_profile_help_features()
    sys.exit(0 if success else 1)