"""
API Views for Chemical Equipment Parameter Visualizer
Django 5 + DRF - Python 3.12 compatible
"""

from __future__ import annotations

from typing import Any
from django.http import HttpRequest, HttpResponse
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser

from equipment.models import Dataset
from .serializers import (
    DatasetListSerializer,
    DatasetDetailSerializer,
    SummarySerializer,
    FileUploadSerializer,
    UploadResponseSerializer,
    ErrorResponseSerializer,
)
from .services import CSVProcessingService, StatisticsService
from .pdf_generator import generate_pdf_report


class UploadCSVView(APIView):
    """
    POST /api/upload/
    Accept CSV file, validate columns, process with pandas, store dataset.
    Keeps only last 5 datasets per user (or globally for anonymous).
    Associates dataset with authenticated user if logged in.
    """
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request: Request) -> Response:
        """Handle CSV file upload"""
        serializer = FileUploadSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                ErrorResponseSerializer({
                    'error': 'Invalid upload',
                    'details': [str(e) for errors in serializer.errors.values() for e in errors]
                }).data,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        file = serializer.validated_data['file']
        filename = serializer.validated_data.get('filename') or None
        
        # Get user if authenticated (for ownership)
        user = request.user if request.user.is_authenticated else None
        
        # Process file using service
        result = CSVProcessingService.process_file(file, filename, user=user)
        
        if not result['success']:
            return Response(
                ErrorResponseSerializer({
                    'error': result['error'] or 'Upload failed',
                    'details': []
                }).data,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get summary for response
        summary = StatisticsService.calculate_from_dataset(result['dataset_id'])
        
        response_data = {
            'success': True,
            'dataset_id': result['dataset_id'],
            'message': f"Successfully uploaded dataset with {summary['total_count']} records",
            'summary': summary
        }
        
        return Response(
            UploadResponseSerializer(response_data).data,
            status=status.HTTP_201_CREATED
        )


class SummaryView(APIView):
    """
    GET /api/summary/<id>/
    Return dataset statistics:
    - total count
    - avg flowrate
    - avg pressure  
    - avg temperature
    - type distribution
    """
    permission_classes = [AllowAny]
    
    def get(self, request: Request, pk: int) -> Response:
        """Get dataset summary statistics"""
        # Verify dataset exists
        if not Dataset.objects.filter(pk=pk).exists():
            return Response(
                ErrorResponseSerializer({
                    'error': f'Dataset with id {pk} not found',
                    'details': []
                }).data,
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Calculate statistics
        summary = StatisticsService.calculate_from_dataset(pk)
        
        if summary is None:
            return Response(
                ErrorResponseSerializer({
                    'error': 'Failed to calculate statistics',
                    'details': []
                }).data,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        return Response(SummarySerializer(summary).data)


class DatasetListView(generics.ListAPIView):
    """
    GET /api/datasets/
    List datasets (history), ordered by upload date.
    - Authenticated users: see only their datasets
    - Anonymous users: see all anonymous datasets (no owner)
    """
    serializer_class = DatasetListSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        """Return datasets filtered by user ownership"""
        if self.request.user.is_authenticated:
            # Authenticated user: return their datasets
            return Dataset.objects.filter(user=self.request.user).order_by('-uploaded_at')
        else:
            # Anonymous: return datasets with no owner
            return Dataset.objects.filter(user__isnull=True).order_by('-uploaded_at')


class DatasetDetailView(generics.RetrieveDestroyAPIView):
    """
    GET /api/datasets/<id>/
    DELETE /api/datasets/<id>/
    Get or delete a specific dataset with all records.
    """
    serializer_class = DatasetDetailSerializer
    permission_classes = [AllowAny]
    queryset = Dataset.objects.all()
    
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Delete dataset and its file"""
        instance = self.get_object()
        if instance.csv_file:
            instance.csv_file.delete(save=False)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReportView(APIView):
    """
    GET /api/report/<id>/
    Generate and download PDF report for dataset.
    """
    permission_classes = [AllowAny]
    
    def get(self, request: Request, pk: int) -> HttpResponse:
        """Generate PDF report"""
        try:
            dataset = Dataset.objects.get(pk=pk)
        except Dataset.DoesNotExist:
            return Response(
                ErrorResponseSerializer({
                    'error': f'Dataset with id {pk} not found',
                    'details': []
                }).data,
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Generate PDF
        pdf_buffer = generate_pdf_report(dataset)
        
        # Create response
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{dataset.filename}_report.pdf"'
        
        return response
