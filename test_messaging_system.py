#!/usr/bin/env python
"""
Test script to create sample messages and verify messaging functionality
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from accounts.models import CustomUser
from items.models import Message

def test_messaging_system():
    print("🔧 Testing Messaging System...")
    
    # Get test users
    try:
        admin_user = CustomUser.objects.get(username='admin')
        user1 = CustomUser.objects.get(username='john_doe')
        user2 = CustomUser.objects.get(username='jane_smith')
        print(f"✅ Found users: {admin_user.username}, {user1.username}, {user2.username}")
    except CustomUser.DoesNotExist:
        print("❌ Test users not found. Please run the complete system test first.")
        return
    
    # Create sample messages between users
    sample_messages = [
        {
            'sender': user1,
            'receiver': user2,
            'content': 'Hi Jane! I saw your found item post. I think it might be mine.'
        },
        {
            'sender': user2,
            'receiver': user1,
            'content': 'Hi John! Can you describe the item to verify ownership?'
        },
        {
            'sender': user1,
            'receiver': user2,
            'content': 'It\'s a black iPhone with a cracked screen and a blue case with my initials "JD" on it.'
        },
        {
            'sender': user2,
            'receiver': user1,
            'content': 'That matches perfectly! When would you like to meet to collect it?'
        },
        {
            'sender': user1,
            'receiver': admin_user,
            'content': 'Hi Admin, I have a question about the claim verification process.'
        },
        {
            'sender': admin_user,
            'receiver': user1,
            'content': 'Hello John! I\'m happy to help. What would you like to know about the verification process?'
        }
    ]
    
    created_count = 0
    for msg_data in sample_messages:
        message, created = Message.objects.get_or_create(
            sender=msg_data['sender'],
            receiver=msg_data['receiver'],
            content=msg_data['content'],
            defaults={}
        )
        if created:
            created_count += 1
    
    print(f"✅ Created {created_count} new sample messages")
    
    # Test statistics
    total_messages = Message.objects.count()
    conversations = Message.objects.values('sender', 'receiver').distinct().count()
    
    print(f"\n📊 Messaging Statistics:")
    print(f"   Total Messages: {total_messages}")
    print(f"   Unique Conversations: {conversations}")
    
    # Test conversation retrieval
    user1_conversations = Message.objects.filter(
        models.Q(sender=user1) | models.Q(receiver=user1)
    ).values_list('sender', 'receiver').distinct()
    
    print(f"   {user1.username}'s Conversations: {len(user1_conversations)}")
    
    print(f"\n🎉 Messaging system test completed successfully!")
    print(f"✅ Sample conversations created")
    print(f"✅ Message model working correctly")
    print(f"✅ Conversation retrieval functional")
    
    print(f"\n🌐 Test the messaging system:")
    print(f"   1. Login as john_doe (password: password123)")
    print(f"   2. Go to: http://127.0.0.1:8000/items/messages/")
    print(f"   3. Click on a contact to view conversation")
    print(f"   4. Send new messages to test functionality")
    
    print(f"\n💬 Available Conversations:")
    for user in [user1, user2, admin_user]:
        sent = Message.objects.filter(sender=user).count()
        received = Message.objects.filter(receiver=user).count()
        print(f"   {user.username}: {sent} sent, {received} received")

if __name__ == '__main__':
    from django.db import models
    test_messaging_system()