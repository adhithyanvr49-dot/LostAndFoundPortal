# items/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('report/', views.report_item, name='report_item'),
    path('my-reports/', views.my_reports, name='my_reports'), # Add this line
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('global-feed/', views.item_list, name='item_list'), 
    path('messages/', views.messages_view, name='my_messages'),
    path('claim-history/', views.claim_history, name='claim_history'),
    path('auto-matches/', views.auto_matches, name='auto_matches'),
    path('map-view/', views.map_view, name='map_view'),
]

