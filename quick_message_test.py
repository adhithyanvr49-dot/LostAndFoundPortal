#!/usr/bin/env python
"""
Quick test to verify messaging system
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from accounts.models import CustomUser
from items.models import Message
from django.db.models import Q

def quick_test():
    print("🔧 Quick Messaging Test...")
    
    # Get sujith user
    sujith = CustomUser.objects.get(username='sujith')
    print(f"Testing for user: {sujith.username}")
    
    # Get contacts for sujith
    sent = Message.objects.filter(sender=sujith).values_list('receiver', flat=True)
    received = Message.objects.filter(receiver=sujith).values_list('sender', flat=True)
    contact_ids = set(list(sent) + list(received))
    contact_ids.discard(sujith.id)
    contacts = CustomUser.objects.filter(id__in=contact_ids)
    
    print(f"Contacts found: {contacts.count()}")
    for contact in contacts:
        print(f"  - {contact.username} (ID: {contact.id})")
        
        # Get messages with this contact
        messages = Message.objects.filter(
            Q(sender=sujith, receiver=contact) | 
            Q(sender=contact, receiver=sujith)
        ).order_by('timestamp')
        
        print(f"    Messages: {messages.count()}")
        for msg in messages:
            print(f"      {msg.sender.username}: {msg.content[:30]}...")
    
    print(f"\n✅ Data is ready!")
    print(f"🌐 Test URLs:")
    print(f"   Debug: http://127.0.0.1:8000/items/messages-debug/")
    print(f"   Normal: http://127.0.0.1:8000/items/messages/")
    print(f"   With contact: http://127.0.0.1:8000/items/messages/4/")

if __name__ == '__main__':
    quick_test()