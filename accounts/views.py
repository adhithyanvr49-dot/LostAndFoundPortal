# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from .forms import CustomUserCreationForm, AdminLoginForm
from .models import CustomUser

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def custom_login_view(request):
    if request.method == 'POST':
        form = AdminLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user_type = form.cleaned_data.get('user_type')
            
            user = authenticate(username=username, password=password)
            if user is not None:
                # Update last login attempt
                user.last_login_attempt = timezone.now()
                user.save()
                
                # Check if account is suspended
                if not user.is_account_active():
                    if user.account_status == 'suspended':
                        messages.error(request, f'Your account is temporarily suspended. Reason: {user.suspension_reason or "No reason provided"}. Contact administrator for assistance.')
                    elif user.account_status == 'banned':
                        messages.error(request, 'Your account has been permanently banned. Contact administrator for assistance.')
                    return render(request, 'registration/login.html', {'form': form})
                
                # Check if user type matches
                if user.user_type == user_type:
                    login(request, user)
                    if user_type == 'admin':
                        return redirect('admin_dashboard')
                    else:
                        return redirect('dashboard')
                else:
                    messages.error(request, 'Invalid user type selected.')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AdminLoginForm()
    
    return render(request, 'registration/login.html', {'form': form})

@login_required
def admin_dashboard(request):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    from items.models import Item, Claim
    
    # Admin dashboard statistics
    total_items = Item.objects.count()
    total_users = CustomUser.objects.filter(user_type='normal').count()
    active_users = CustomUser.objects.filter(user_type='normal', account_status='active').count()
    suspended_users = CustomUser.objects.filter(user_type='normal', account_status='suspended').count()
    
    pending_claims = Claim.objects.filter(status='PENDING').count()
    approved_claims = Claim.objects.filter(status='APPROVED').count()
    rejected_claims = Claim.objects.filter(status='REJECTED').count()
    
    # Recent claims for verification
    recent_claims = Claim.objects.filter(status='PENDING').order_by('-created_at')[:10]
    
    # Recent user activity
    recent_users = CustomUser.objects.filter(user_type='normal').order_by('-date_joined')[:5]
    
    context = {
        'total_items': total_items,
        'total_users': total_users,
        'active_users': active_users,
        'suspended_users': suspended_users,
        'pending_claims': pending_claims,
        'approved_claims': approved_claims,
        'rejected_claims': rejected_claims,
        'recent_claims': recent_claims,
        'recent_users': recent_users,
    }
    
    return render(request, 'admin/admin_dashboard.html', context)

@login_required
def verify_claim(request, claim_id):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    from items.models import Claim
    
    claim = get_object_or_404(Claim, id=claim_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        verification_notes = request.POST.get('verification_notes', '')
        
        if action == 'approve':
            claim.status = 'APPROVED'
            claim.verified_by = request.user
            claim.verification_date = timezone.now()
            claim.verification_notes = verification_notes
            messages.success(request, f'Claim for "{claim.item.title}" has been approved.')
        elif action == 'reject':
            claim.status = 'REJECTED'
            claim.verified_by = request.user
            claim.verification_date = timezone.now()
            claim.verification_notes = verification_notes
            messages.success(request, f'Claim for "{claim.item.title}" has been rejected.')
        elif action == 'review':
            claim.status = 'UNDER_REVIEW'
            claim.verification_notes = verification_notes
            messages.info(request, f'Claim for "{claim.item.title}" is now under review.')
        
        claim.save()
        return redirect('admin_dashboard')
    
    return render(request, 'admin/verify_claim.html', {'claim': claim})

@login_required
def manage_users(request):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    # Get all normal users
    users_list = CustomUser.objects.filter(user_type='normal').order_by('-date_joined')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        users_list = users_list.filter(
            username__icontains=search_query
        ) | users_list.filter(
            email__icontains=search_query
        )
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        users_list = users_list.filter(account_status=status_filter)
    
    # Pagination
    paginator = Paginator(users_list, 20)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    
    context = {
        'users': users,
        'search_query': search_query,
        'status_filter': status_filter,
        'total_users': users_list.count(),
    }
    
    return render(request, 'admin/manage_users.html', context)

@login_required
def suspend_user(request, user_id):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    user = get_object_or_404(CustomUser, id=user_id, user_type='normal')
    
    if request.method == 'POST':
        reason = request.POST.get('reason', 'Account suspended by administrator')
        user.suspend_account(request.user, reason)
        messages.success(request, f'User "{user.username}" has been suspended.')
        return redirect('manage_users')
    
    return render(request, 'admin/suspend_user.html', {'target_user': user})

@login_required
def reactivate_user(request, user_id):
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    user = get_object_or_404(CustomUser, id=user_id, user_type='normal')
    
    if request.method == 'POST':
        user.reactivate_account()
        messages.success(request, f'User "{user.username}" has been reactivated.')
        return redirect('manage_users')
    
    return render(request, 'admin/reactivate_user.html', {'target_user': user})

def custom_logout_view(request):
    """Custom logout view that handles both admin and normal user logout"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')