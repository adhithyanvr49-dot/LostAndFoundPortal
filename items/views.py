from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Item
from .forms import ItemReportForm 
# items/views.py
from django.shortcuts import render, get_object_or_404
from .models import Item

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
def messages_view(request):
    # This renders the new messaging interface
    return render(request, 'items/messages.html')
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
    categories = user_lost.values_list('category', flat=True)
    
    # Find items found by OTHERS in the same categories
    matches = Item.objects.filter(
        status='FOUND', 
        category__in=categories
    ).exclude(user=request.user)
    
    return render(request, 'items/auto_matches.html', {'matches': matches})

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