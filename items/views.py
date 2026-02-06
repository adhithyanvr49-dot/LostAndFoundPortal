from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from django.contrib.auth import get_user_model
from .forms import ItemReportForm 
from .models import Message, Item, Claim

def item_detail(request, pk):
    # Retrieve the item by its Primary Key (pk)
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'items/item_detail.html', {'item': item})



# items/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Item

@login_required
def dashboard(request):
    user_items = Item.objects.filter(user=request.user)
    
    # Smart Matching Logic: Find FOUND items matching user's LOST categories
    lost_categories = user_items.filter(status='LOST').values_list('category', flat=True)
    potential_matches = Item.objects.filter(
        status='FOUND', 
        category__in=lost_categories
    ).exclude(user=request.user)[:3]

    context = {
        'lost_count': user_items.filter(status='LOST').count(),
        'found_count': user_items.filter(status='FOUND').count(),
        'my_items': user_items.order_by('-created_at')[:5],
        'potential_matches': potential_matches,
    }
    return render(request, 'items/dashboard.html', context)

# Add these placeholder functions to fix the AttributeErrors
def item_list(request):
    items = Item.objects.all().order_by('-created_at')
    return render(request, 'items/item_list.html', {'items': items})
# items/views.py
@login_required
def claim_history(request):
    # This renders the claim history page for the logged-in user
    return render(request, 'items/claim_history.html')
@login_required
def report_item(request):
    if request.method == 'POST':
        form = ItemReportForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            return redirect('dashboard')
    else:
        form = ItemReportForm()
    return render(request, 'items/report_form.html', {'form': form})
# items/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Item

@login_required
def auto_matches(request):
    # Find user's LOST items
    user_lost = Item.objects.filter(user=request.user, status='LOST')
    lost_categories = user_lost.values_list('category', flat=True).distinct()
    
    # Find items found by OTHERS in the same categories
    potential_matches = Item.objects.filter(
        status='FOUND', 
        category__in=lost_categories
    ).exclude(user=request.user).order_by('-created_at')
    
    # Also find items where others lost similar items to what user found
    user_found = Item.objects.filter(user=request.user, status='FOUND')
    found_categories = user_found.values_list('category', flat=True).distinct()
    
    # Find lost items by others in categories user has found items
    reverse_matches = Item.objects.filter(
        status='LOST',
        category__in=found_categories
    ).exclude(user=request.user).order_by('-created_at')
    
    # Get statistics
    total_lost = user_lost.count()
    total_found = user_found.count()
    matches_count = potential_matches.count()
    reverse_matches_count = reverse_matches.count()
    
    context = {
        'user_lost_items': user_lost,
        'user_found_items': user_found,
        'potential_matches': potential_matches,
        'reverse_matches': reverse_matches,
        'total_lost': total_lost,
        'total_found': total_found,
        'matches_count': matches_count,
        'reverse_matches_count': reverse_matches_count,
        'lost_categories': list(lost_categories),
        'found_categories': list(found_categories),
    }
    
    return render(request, 'items/auto_matches.html', context)

@login_required
def map_view(request):
    # Fetch all items to show on the map
    items = Item.objects.all()
    return render(request, 'items/map_view.html', {'items': items})

# ADD THIS FUNCTION to fix the 'item_list' error
# items/views.py
def item_list(request):
    # Fetch all items from all users
    items = Item.objects.all().order_by('-created_at')
    
    # Search logic
    query = request.GET.get('q')
    category = request.GET.get('category')
    
    if query:
        items = items.filter(title__icontains=query)
    if category and category != 'All':
        items = items.filter(category=category.lower())
        
    return render(request, 'items/item_list.html', {'items': items})
@login_required
def my_reports(request):
    # Fetch all items reported by the current user
    reports = Item.objects.filter(user=request.user).order_by('-created_at')
    
    # Handle search/filter logic if the search button is pressed
    query = request.GET.get('q')
    category = request.GET.get('category')
    status = request.GET.get('status')

    if query:
        reports = reports.filter(title__icontains=query)
    if category and category != 'All Categories':
        reports = reports.filter(category=category.lower())
    if status and status != 'All Status':
        reports = reports.filter(status=status.upper())

    return render(request, 'items/my_reports.html', {'my_items': reports})
# items/views.py
# items/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Item, Claim # Ensure Claim is imported now

@login_required
def profile_settings(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        
        # Update user information
        if username and username != request.user.username:
            # Check if username is already taken
            User = get_user_model()
            if User.objects.filter(username=username).exclude(id=request.user.id).exists():
                messages.error(request, 'Username is already taken.')
            else:
                request.user.username = username
                request.user.save()
                messages.success(request, 'Username updated successfully!')
        
        if email and email != request.user.email:
            request.user.email = email
            request.user.save()
            messages.success(request, 'Email updated successfully!')
        
        return redirect('profile_settings')
    
    return render(request, 'items/profile_settings.html')

@login_required
def help_safety(request):
    return render(request, 'items/help_safety.html')

@login_required
def claim_history(request):
    # This powers the 'Claim History' table
    claims = Claim.objects.filter(claimant=request.user)
    return render(request, 'items/claim_history.html', {'claims': claims})
# items/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message

@login_required
def my_messages(request, receiver_id=None):
    # If no receiver is selected, default to the last person messaged
    receiver = None
    if receiver_id:
        receiver = get_object_or_404(User, id=receiver_id)
    
    # Handle sending a new message
    if request.method == 'POST' and receiver:
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, receiver=receiver, content=content)
            return redirect('my_messages', receiver_id=receiver_id)

    # Fetch chat history between current user and the receiver
    chat_messages = []
    if receiver:
        chat_messages = Message.objects.filter(
            models.Q(sender=request.user, receiver=receiver) | 
            models.Q(sender=receiver, receiver=request.user)
        )

    # Get a list of unique people the user has chatted with for the sidebar
    conversations = Message.objects.filter(
        models.Q(sender=request.user) | models.Q(receiver=request.user)
    ).values_list('sender', 'receiver')
    
    # Flatten and find unique users (excluding yourself)
    user_ids = set([uid for conv in conversations for uid in conv if uid != request.user.id])
    contacts = User.objects.filter(id__in=user_ids)

    return render(request, 'items/my_messages.html', {
        'contacts': contacts,
        'receiver': receiver,
        'chat_messages': chat_messages
    })
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib.auth import get_user_model # Use this to fetch the active user model
from .models import Message

User = get_user_model() # This ensures you use 'accounts.CustomUser'

# items/views.py
from django.db.models import Q

@login_required
def messages_view(request, receiver_id=None):
    User = get_user_model()
    receiver = None
    
    if receiver_id:
        receiver = get_object_or_404(User, id=receiver_id)

    if request.method == "POST" and receiver:
        content = request.POST.get('content')
        if content:
            # Save the message to the database
            Message.objects.create(sender=request.user, receiver=receiver, content=content)
            messages.success(request, 'Message sent successfully!')
            # Redirect back to the same chat to see the new message
            return redirect('messages_view', receiver_id=receiver.id)

    # Fetch messages between the logged-in user and the selected receiver
    chat_messages = []
    if receiver:
        chat_messages = Message.objects.filter(
            Q(sender=request.user, receiver=receiver) | 
            Q(sender=receiver, receiver=request.user)
        ).order_by('timestamp')

    # Get a list of unique people the user has chatted with for the sidebar
    sent_messages = Message.objects.filter(sender=request.user).values_list('receiver', flat=True)
    received_messages = Message.objects.filter(receiver=request.user).values_list('sender', flat=True)
    
    # Combine and get unique user IDs
    contact_ids = set(list(sent_messages) + list(received_messages))
    contact_ids.discard(request.user.id)  # Remove self from contacts
    contacts = User.objects.filter(id__in=contact_ids)

    context = {
        'receiver': receiver,
        'chat_messages': chat_messages,
        'contacts': contacts
    }
    
    return render(request, 'items/messages.html', context)

@login_required
def messages_debug(request, receiver_id=None):
    """Debug version of messages view"""
    User = get_user_model()
    receiver = None
    
    if receiver_id:
        receiver = get_object_or_404(User, id=receiver_id)

    # Fetch messages between the logged-in user and the selected receiver
    chat_messages = []
    if receiver:
        chat_messages = Message.objects.filter(
            Q(sender=request.user, receiver=receiver) | 
            Q(sender=receiver, receiver=request.user)
        ).order_by('timestamp')

    # Get contacts
    sent_messages = Message.objects.filter(sender=request.user).values_list('receiver', flat=True)
    received_messages = Message.objects.filter(receiver=request.user).values_list('sender', flat=True)
    contact_ids = set(list(sent_messages) + list(received_messages))
    contact_ids.discard(request.user.id)
    contacts = User.objects.filter(id__in=contact_ids)

    return render(request, 'items/messages_debug.html', {
        'receiver': receiver,
        'chat_messages': chat_messages,
        'contacts': contacts
    })

@login_required
def start_conversation(request, user_id):
    """Start a conversation with another user"""
    User = get_user_model()
    other_user = get_object_or_404(User, id=user_id)
    
    # Check if there's already a conversation
    existing_messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) | 
        Q(sender=other_user, receiver=request.user)
    ).exists()
    
    if not existing_messages:
        # Create an initial message to start the conversation
        Message.objects.create(
            sender=request.user,
            receiver=other_user,
            content=f"Hi {other_user.username}, I'm interested in discussing an item with you."
        )
        messages.success(request, f'Conversation started with {other_user.username}')
    
    return redirect('messages_view', receiver_id=other_user.id)
# items/views.py# items/views.py
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Item, Claim # Ensure Claim model is imported

@login_required
def claim_item(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(Item, id=item_id)
        proof = request.POST.get('proof_description')
        claim_type = request.POST.get('claim_type', 'ownership')
        
        # Check if user is claiming their own item
        if claim_type == 'found_my_item' and item.user != request.user:
            messages.error(request, 'You can only claim your own reported items.')
            return redirect('item_detail', pk=item_id)
        
        # Check if user already has a pending claim for this item
        existing_claim = Claim.objects.filter(
            item=item, 
            claimant=request.user, 
            status__in=['PENDING', 'UNDER_REVIEW']
        ).first()
        
        if existing_claim:
            messages.warning(request, 'You already have a pending claim for this item.')
            return redirect('claim_history')
        
        # Save the claim to the database
        Claim.objects.create(
            item=item,
            claimant=request.user,
            claim_type=claim_type,
            proof_description=proof,
            status='PENDING'
        )
        
        if claim_type == 'found_my_item':
            messages.success(request, 'Your "Found My Item" claim has been submitted for verification.')
        else:
            messages.success(request, 'Your ownership claim has been submitted for verification.')
            
        return redirect('claim_history')
    
    return redirect('dashboard')

@login_required
def submit_claim_form(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    
    # Determine claim type based on ownership
    is_own_item = item.user == request.user
    
    context = {
        'item': item,
        'is_own_item': is_own_item,
    }
    
    return render(request, 'items/submit_claim.html', context)
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Claim 

@login_required
def delete_claim(request, claim_id):
    # Retrieve the claim or return 404
    claim = get_object_or_404(Claim, id=claim_id)
    
    # Security: Ensure only the person who created the claim can delete it
    if claim.claimant == request.user:
        claim.delete()
        
    # Redirect back to the claim history page
    return redirect('claim_history')
