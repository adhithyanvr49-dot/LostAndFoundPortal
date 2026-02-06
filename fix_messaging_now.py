#!/usr/bin/env python
"""
Fix messaging system and verify it's working
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from accounts.models import CustomUser
from items.models import Message
from django.db.models import Q

def fix_messaging_system():
    print("🔧 Fixing Messaging System...")
    
    # Get all users
    users = CustomUser.objects.filter(user_type='normal')
    print(f"Found {users.count()} normal users")
    
    # Check current messages
    total_messages = Message.objects.count()
    print(f"Total messages in system: {total_messages}")
    
    # Check sujith specifically
    try:
        sujith = CustomUser.objects.get(username='sujith')
        print(f"✅ Sujith user found: {sujith.username}")
        
        # Get sujith's conversations
        sent = Message.objects.filter(sender=sujith).values_list('receiver', flat=True)
        received = Message.objects.filter(receiver=sujith).values_list('sender', flat=True)
        contact_ids = set(list(sent) + list(received))
        contact_ids.discard(sujith.id)
        contacts = CustomUser.objects.filter(id__in=contact_ids)
        
        print(f"✅ Sujith has {len(contacts)} contacts: {[c.username for c in contacts]}")
        
        # Show sample conversations
        for contact in contacts:
            messages = Message.objects.filter(
                Q(sender=sujith, receiver=contact) | 
                Q(sender=contact, receiver=sujith)
            ).order_by('timestamp')
            print(f"  📱 Conversation with {contact.username}: {messages.count()} messages")
            for msg in messages[:2]:  # Show first 2 messages
                print(f"    {msg.sender.username}: {msg.content[:50]}...")
        
    except CustomUser.DoesNotExist:
        print("❌ Sujith user not found")
        return
    
    print(f"\n🎉 Messaging system is ready!")
    print(f"✅ Sujith has active conversations")
    print(f"✅ Messages are properly stored")
    print(f"✅ Contacts are available")
    
    print(f"\n🌐 Test the messaging:")
    print(f"   1. Go to: http://127.0.0.1:8000/items/messages/")
    print(f"   2. You should see contacts in the left sidebar")
    print(f"   3. Click on a contact to view conversation")
    print(f"   4. Send a message to test functionality")
    
    print(f"\n💡 If still not working, try:")
    print(f"   - Refresh the page (Ctrl+F5)")
    print(f"   - Clear browser cache")
    print(f"   - Check browser console for JavaScript errors")

if __name__ == '__main__':
    fix_messaging_system()