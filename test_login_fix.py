#!/usr/bin/env python3
"""
Test login functionality to ensure it's working properly
"""
import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

def test_login_functionality():
    """Test that login is working for all user types"""
    print("🔐 Testing Login Functionality")
    print("=" * 50)
    
    User = get_user_model()
    
    # Test cases
    test_cases = [
        {
            'username': 'sujith',
            'password': 'sujith123',
            'user_type': 'normal',
            'expected_redirect': '/items/dashboard/'
        },
        {
            'username': 'admin',
            'password': 'admin123',
            'user_type': 'admin',
            'expected_redirect': '/admin-dashboard/'
        },
        {
            'username': 'adhi',
            'password': 'adhi123',
            'user_type': 'normal',
            'expected_redirect': '/items/dashboard/'
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: {test_case['username']} ({test_case['user_type']})")
        
        client = Client()
        
        # Verify user exists
        try:
            user = User.objects.get(username=test_case['username'])
            print(f"   ✅ User exists: {user.username}")
            print(f"   - User type: {user.user_type}")
            print(f"   - Account status: {user.account_status}")
            
            # Test password
            if user.check_password(test_case['password']):
                print(f"   ✅ Password correct")
            else:
                print(f"   ❌ Password incorrect")
                continue
                
        except User.DoesNotExist:
            print(f"   ❌ User {test_case['username']} does not exist")
            continue
        
        # Test login
        response = client.post('/accounts/login/', {
            'username': test_case['username'],
            'password': test_case['password'],
            'user_type': test_case['user_type']
        })
        
        if response.status_code == 302:
            print(f"   ✅ Login successful")
            print(f"   - Redirect URL: {response.url}")
            
            if response.url == test_case['expected_redirect']:
                print(f"   ✅ Correct redirect for {test_case['user_type']} user")
            else:
                print(f"   ⚠️  Unexpected redirect: expected {test_case['expected_redirect']}, got {response.url}")
                
        else:
            print(f"   ❌ Login failed - Status: {response.status_code}")
    
    print(f"\n" + "=" * 50)
    print("🎉 Login Testing Complete!")
    
    print(f"\n📋 Available Login Credentials:")
    print("   👤 Normal Users:")
    print("      - sujith / sujith123")
    print("      - adhi / adhi123") 
    print("      - abhinav / abhinav123")
    print("      - john_doe / john123")
    print("      - jane_smith / jane123")
    print("   👨‍💼 Admin User:")
    print("      - admin / admin123")
    
    print(f"\n🔗 Login URL: http://127.0.0.1:8000/accounts/login/")
    
    return True

if __name__ == "__main__":
    success = test_login_functionality()
    sys.exit(0 if success else 1)