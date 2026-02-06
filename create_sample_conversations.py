#!/usr/bin/env python3
"""
Create sample conversations between users to demonstrate messaging functionality
"""
import os
import django
import sys
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from items.models import Message
from django.utils import timezone

def create_sample_conversations():
    """Create realistic sample conversations between users"""
    print("💬 Creating Sample Conversations")
    print("=" * 50)
    
    User = get_user_model()
    
    # Get users
    try:
        users = {
            'sujith': User.objects.get(username='sujith_updated'),
            'abhinav': User.objects.get(username='abhinav'),
            'admin': User.objects.get(username='admin'),
            'john': User.objects.get(username='john_doe'),
            'jane': User.objects.get(username='jane_smith'),
            'adhi': User.objects.get(username='adhi'),
        }
        print(f"✅ Found {len(users)} users for conversations")
    except User.DoesNotExist as e:
        print(f"❌ Some users not found: {e}")
        return False
    
    # Clear existing messages for fresh start
    Message.objects.all().delete()
    print("✅ Cleared existing messages")
    
    # Conversation 1: sujith_updated and abhinav about a lost phone
    conversations = [
        {
            'participants': ['sujith', 'abhinav'],
            'messages': [
                ('sujith', 'Hi abhinav! I saw your post about the lost iPhone. I think I found it!'),
                ('abhinav', 'Really? That would be amazing! Where did you find it?'),
                ('sujith', 'I found it near the library yesterday evening. It has a blue case with some stickers.'),
                ('abhinav', 'Yes! That sounds exactly like mine. The stickers are from my favorite band.'),
                ('sujith', 'Perfect! When would be a good time to meet? I can bring it to the campus cafe.'),
                ('abhinav', 'How about tomorrow at 2 PM? I really appreciate you finding it!'),
                ('sujith', 'Sounds great! See you at the cafe at 2 PM tomorrow. Glad I could help!'),
            ]
        },
        {
            'participants': ['john', 'jane'],
            'messages': [
                ('john', 'Hey Jane, I lost my wallet near the gym. Have you seen anything?'),
                ('jane', 'Hi John! I actually found a brown leather wallet this morning. Is it yours?'),
                ('john', 'Brown leather with a small tear on the corner? That might be it!'),
                ('jane', 'Yes, exactly! It has your student ID in it. Want to meet at the student center?'),
                ('john', 'That would be perfect! Thank you so much. How about in an hour?'),
                ('jane', 'Sure, see you at the main entrance in an hour. Happy to help!'),
            ]
        },
        {
            'participants': ['adhi', 'admin'],
            'messages': [
                ('adhi', 'Hello admin, I have a question about the claim verification process.'),
                ('admin', 'Hi adhi! I am here to help. What would you like to know?'),
                ('adhi', 'How long does it usually take for claims to be verified?'),
                ('admin', 'Typically 24-48 hours. We review all proof documents carefully to ensure legitimate claims.'),
                ('adhi', 'That makes sense. What kind of proof works best for electronics?'),
                ('admin', 'Photos of the item, purchase receipts, or unique identifying features work well. Serial numbers are especially helpful.'),
                ('adhi', 'Great, thank you for the information!'),
            ]
        },
        {
            'participants': ['jane', 'sujith'],
            'messages': [
                ('jane', 'Hi! I saw you posted about finding a set of keys. Are they still available?'),
                ('sujith', 'Yes, I still have them! They have a red keychain with a small flashlight.'),
                ('jane', 'Those might be mine! I lost them last week near the parking lot.'),
                ('sujith', 'That is where I found them! Can you describe any other details?'),
                ('jane', 'There should be 3 keys - one car key, one house key, and a small mailbox key.'),
                ('sujith', 'Perfect match! When can you pick them up?'),
            ]
        },
        {
            'participants': ['abhinav', 'admin'],
            'messages': [
                ('abhinav', 'Hi admin, I submitted a claim yesterday but have not heard back yet.'),
                ('admin', 'Let me check on that for you. What item did you claim?'),
                ('abhinav', 'It was the iPhone found near the library. I provided photos and my purchase receipt.'),
                ('admin', 'I see your claim. Everything looks good! I will approve it shortly. The finder will be notified.'),
                ('abhinav', 'Excellent! Thank you for the quick response.'),
            ]
        }
    ]
    
    # Create conversations with realistic timestamps
    base_time = timezone.now() - timedelta(days=2)
    
    for conv_idx, conversation in enumerate(conversations):
        participants = conversation['participants']
        messages = conversation['messages']
        
        print(f"\n📝 Creating conversation between {participants[0]} and {participants[1]}:")
        
        for msg_idx, (sender_key, content) in enumerate(messages):
            sender = users[sender_key]
            receiver_key = participants[1] if sender_key == participants[0] else participants[0]
            receiver = users[receiver_key]
            
            # Create message with incremental timestamp
            timestamp = base_time + timedelta(
                hours=conv_idx * 6,  # Space conversations apart
                minutes=msg_idx * 15  # Space messages within conversation
            )
            
            message = Message.objects.create(
                sender=sender,
                receiver=receiver,
                content=content,
                timestamp=timestamp
            )
            
            print(f"   {sender.username}: {content[:50]}...")
    
    # Summary
    total_messages = Message.objects.count()
    total_conversations = len(conversations)
    unique_participants = len(set([p for conv in conversations for p in conv['participants']]))
    
    print(f"\n" + "=" * 50)
    print("🎉 Sample Conversations Created Successfully!")
    print(f"\n📊 Statistics:")
    print(f"   💬 Total Messages: {total_messages}")
    print(f"   🗣️  Total Conversations: {total_conversations}")
    print(f"   👥 Unique Participants: {unique_participants}")
    
    print(f"\n📋 Conversation Topics:")
    print("   📱 Lost iPhone recovery")
    print("   💳 Wallet found at gym")
    print("   ❓ Admin support questions")
    print("   🔑 Key return coordination")
    print("   ✅ Claim status updates")
    
    print(f"\n🔗 Users can now test messaging at:")
    print("   http://127.0.0.1:8000/items/messages/")
    
    return True

if __name__ == "__main__":
    success = create_sample_conversations()
    sys.exit(0 if success else 1)