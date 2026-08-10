"""
API URL Configuration
Chemical Equipment Parameter Visualizer
"""

from django.urls import path
from . import views
from . import auth_views

urlpatterns = [
    # Health check
    path('', views.APIHealthView.as_view(), name='api-health'),

    # =========================================================================
    # Authentication Endpoints
    # =========================================================================
    path('auth/register/', auth_views.RegisterView.as_view(), name='auth-register'),
    path('auth/login/', auth_views.LoginView.as_view(), name='auth-login'),
    path('auth/logout/', auth_views.LogoutView.as_view(), name='auth-logout'),
    path('auth/user/', auth_views.UserProfileView.as_view(), name='auth-user'),
    
    # =========================================================================
    # Data Endpoints
    # =========================================================================
    # Upload endpoint
    path('upload/', views.UploadCSVView.as_view(), name='upload'),
    
    # Summary endpoint  
    path('summary/<int:pk>/', views.SummaryView.as_view(), name='summary'),
    
    # Dataset list (history)
    path('datasets/', views.DatasetListView.as_view(), name='dataset-list'),
    
    # PDF Report
    path('report/<int:pk>/', views.ReportView.as_view(), name='report'),
    
    # Dataset detail with records
    path('datasets/<int:pk>/', views.DatasetDetailView.as_view(), name='dataset-detail'),
]
