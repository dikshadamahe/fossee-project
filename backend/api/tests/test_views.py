"""
Unit Tests for API Views
Django 5 + Python 3.12 compatible
"""

from __future__ import annotations

import json
from unittest.mock import patch, MagicMock

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.core.files.uploadedfile import SimpleUploadedFile

from equipment.models import Dataset, EquipmentRecord


class UploadCSVViewTests(APITestCase):
    """Tests for CSV upload endpoint"""
    
    def setUp(self) -> None:
        """Set up test client"""
        self.client = APIClient()
        self.url = '/api/upload/'
    
    def _create_csv_file(
        self, 
        content: str | None = None, 
        filename: str = "test.csv"
    ) -> SimpleUploadedFile:
        """Helper to create CSV file for testing"""
        if content is None:
            content = (
                "Equipment Name,Type,Flowrate,Pressure,Temperature\n"
                "Pump A,Centrifugal,100.5,50.2,25.0\n"
                "Valve B,Gate,75.3,40.1,30.5\n"
            )
        return SimpleUploadedFile(
            filename,
            content.encode('utf-8'),
            content_type="text/csv"
        )
    
    def test_upload_valid_csv(self) -> None:
        """Test successful CSV upload"""
        csv_file = self._create_csv_file()
        
        response = self.client.post(
            self.url,
            {'file': csv_file},
            format='multipart'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertIn('dataset_id', response.data)
        self.assertIn('summary', response.data)
    
    def test_upload_no_file(self) -> None:
        """Test upload without file"""
        response = self.client.post(self.url, {}, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_upload_invalid_columns(self) -> None:
        """Test upload with invalid columns"""
        csv_file = self._create_csv_file(
            content="Name,Value\nTest,100\n"
        )
        
        response = self.client.post(
            self.url,
            {'file': csv_file},
            format='multipart'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_upload_with_custom_filename(self) -> None:
        """Test upload with custom filename"""
        csv_file = self._create_csv_file()
        
        response = self.client.post(
            self.url,
            {'file': csv_file, 'filename': 'custom_dataset'},
            format='multipart'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        dataset = Dataset.objects.get(pk=response.data['dataset_id'])
        self.assertEqual(dataset.filename, 'custom_dataset')
    
    def test_upload_normalizes_columns(self) -> None:
        """Test that column names are normalized during upload"""
        content = (
            "equipment_name,type,flow_rate,press,temp\n"
            "Pump A,Centrifugal,100.5,50.2,25.0\n"
        )
        csv_file = self._create_csv_file(content=content)
        
        response = self.client.post(
            self.url,
            {'file': csv_file},
            format='multipart'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class SummaryViewTests(APITestCase):
    """Tests for dataset summary endpoint"""
    
    def setUp(self) -> None:
        """Set up test data"""
        self.client = APIClient()
        self.dataset = Dataset.objects.create(filename="test_summary")
        EquipmentRecord.objects.bulk_create([
            EquipmentRecord(
                dataset=self.dataset,
                equipment_name='Pump A',
                type='Centrifugal',
                flowrate=100.0,
                pressure=50.0,
                temperature=25.0
            ),
            EquipmentRecord(
                dataset=self.dataset,
                equipment_name='Pump B',
                type='Centrifugal',
                flowrate=200.0,
                pressure=60.0,
                temperature=30.0
            ),
        ])
    
    def test_get_summary_success(self) -> None:
        """Test getting dataset summary"""
        url = f'/api/summary/{self.dataset.id}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_count'], 2)
        self.assertEqual(response.data['avg_flowrate'], 150.0)
        self.assertEqual(response.data['avg_pressure'], 55.0)
        self.assertEqual(response.data['avg_temperature'], 27.5)
    
    def test_get_summary_not_found(self) -> None:
        """Test summary for non-existent dataset"""
        url = '/api/summary/99999/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)


class DatasetListViewTests(APITestCase):
    """Tests for dataset list endpoint"""
    
    def setUp(self) -> None:
        """Set up test data"""
        self.client = APIClient()
        self.url = '/api/datasets/'
        
        # Create multiple datasets
        for i in range(3):
            Dataset.objects.create(filename=f"test_{i}")
    
    def test_list_datasets(self) -> None:
        """Test listing all datasets"""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
    
    def test_list_datasets_ordered(self) -> None:
        """Test datasets are ordered by upload date"""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Most recent should be first
        self.assertEqual(response.data[0]['filename'], 'test_2')


class DatasetDetailViewTests(APITestCase):
    """Tests for dataset detail endpoint"""
    
    def setUp(self) -> None:
        """Set up test data"""
        self.client = APIClient()
        self.dataset = Dataset.objects.create(filename="test_detail")
        EquipmentRecord.objects.create(
            dataset=self.dataset,
            equipment_name='Pump A',
            type='Centrifugal',
            flowrate=100.0,
            pressure=50.0,
            temperature=25.0
        )
    
    def test_get_dataset_detail(self) -> None:
        """Test getting dataset details"""
        url = f'/api/datasets/{self.dataset.id}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['filename'], 'test_detail')
        self.assertIn('records', response.data)
        self.assertEqual(len(response.data['records']), 1)
    
    def test_get_dataset_not_found(self) -> None:
        """Test detail for non-existent dataset"""
        url = '/api/datasets/99999/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_dataset(self) -> None:
        """Test deleting a dataset"""
        url = f'/api/datasets/{self.dataset.id}/'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Dataset.objects.filter(pk=self.dataset.id).exists())


class ReportViewTests(APITestCase):
    """Tests for PDF report endpoint"""
    
    def setUp(self) -> None:
        """Set up test data"""
        self.client = APIClient()
        self.dataset = Dataset.objects.create(
            filename="test_report",
            summary_json=json.dumps({
                'flowrate': {'min': 100, 'max': 200, 'mean': 150, 'std': 50},
                'pressure': {'min': 50, 'max': 60, 'mean': 55, 'std': 5},
                'temperature': {'min': 25, 'max': 30, 'mean': 27.5, 'std': 2.5},
            })
        )
        EquipmentRecord.objects.create(
            dataset=self.dataset,
            equipment_name='Pump A',
            type='Centrifugal',
            flowrate=100.0,
            pressure=50.0,
            temperature=25.0
        )
    
    def test_get_report_success(self) -> None:
        """Test generating PDF report"""
        url = f'/api/report/{self.dataset.id}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('attachment', response['Content-Disposition'])
    
    def test_get_report_not_found(self) -> None:
        """Test report for non-existent dataset"""
        url = '/api/report/99999/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
