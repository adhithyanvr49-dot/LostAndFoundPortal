# items/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('report/', views.report_item, name='report_item'),
    path('my-reports/', views.my_reports, name='my_reports'), # Add this l
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('global-feed/', views.item_list, name='item_list'), 
    path('messages/', views.messages_view, name='my_messages'),
    path('auto-matches/', views.auto_matches, name='auto_matches'),
    path('claim-history/', views.claim_history, name='claim_history'),
    path('map-view/', views.map_view, name='map_view'),
    path('profile-settings/', views.profile_settings, name='profile_settings'),
    path('messages/', views.messages_view, name='messages_view'),
    path('messages/<int:receiver_id>/', views.messages_view, name='messages_view'),
    # items/urls.py
    path('claim/delete/<int:claim_id>/', views.delete_claim, name='delete_claim'),
    path('claim/<int:item_id>/', views.claim_item, name='claim_item'),
]

