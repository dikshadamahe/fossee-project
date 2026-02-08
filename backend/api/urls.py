"""
API URL Configuration
Chemical Equipment Parameter Visualizer
"""

from django.urls import path
from . import views

urlpatterns = [
    # Upload endpoint
    path('upload/', views.UploadCSVView.as_view(), name='upload'),
    
    # Summary endpoint  
    path('summary/<int:pk>/', views.SummaryView.as_view(), name='summary'),
    
    # Dataset list (history)
    path('datasets/', views.DatasetListView.as_view(), name='dataset-list'),
    
    # PDF Report
    path('report/<int:pk>/', views.ReportView.as_view(), name='report'),
    
    # Optional: Dataset detail with records
    path('datasets/<int:pk>/', views.DatasetDetailView.as_view(), name='dataset-detail'),
]

