"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import landing_page # Import your view
from accounts.views import (
    signup_view, custom_login_view, admin_dashboard, verify_claim,
    manage_users, suspend_user, reactivate_user
)

urlpatterns = [
    
    path('accounts/signup/', signup_view, name='signup'),
    path('accounts/login/', custom_login_view, name='login'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('verify-claim/<int:claim_id>/', verify_claim, name='verify_claim'),
    path('manage-users/', manage_users, name='manage_users'),
    path('suspend-user/<int:user_id>/', suspend_user, name='suspend_user'),
    path('reactivate-user/<int:user_id>/', reactivate_user, name='reactivate_user'),
    path('admin/', admin.site.urls),
    path('', landing_page, name='home'),
    path('items/', include('items.urls')),
    path('accounts/', include('django.contrib.auth.urls')), # Built-in auth
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

