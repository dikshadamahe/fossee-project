"""
Unit Tests for Serializers
Django 5 + Python 3.12 compatible
"""

from __future__ import annotations

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.exceptions import ValidationError

from api.serializers import (
    EquipmentRecordSerializer,
    DatasetListSerializer,
    DatasetDetailSerializer,
    SummarySerializer,
    ExtendedStatisticsSerializer,
    FileUploadSerializer,
    UploadResponseSerializer,
    ErrorResponseSerializer,
)
from equipment.models import Dataset, EquipmentRecord


class EquipmentRecordSerializerTests(TestCase):
    """Tests for EquipmentRecordSerializer"""
    
    def setUp(self) -> None:
        """Set up test data"""
        self.dataset = Dataset.objects.create(filename="test")
        self.record = EquipmentRecord.objects.create(
            dataset=self.dataset,
            equipment_name="Pump A",
            type="Centrifugal",
            flowrate=100.5,
            pressure=50.2,
            temperature=25.0
        )
    
    def test_serialize_record(self) -> None:
        """Test serializing an equipment record"""
        serializer = EquipmentRecordSerializer(self.record)
        data = serializer.data
        
        self.assertEqual(data['equipment_name'], 'Pump A')
        self.assertEqual(data['type'], 'Centrifugal')
        self.assertEqual(float(data['flowrate']), 100.5)
        self.assertEqual(float(data['pressure']), 50.2)
        self.assertEqual(float(data['temperature']), 25.0)


class DatasetListSerializerTests(TestCase):
    """Tests for DatasetListSerializer"""
    
    def test_serialize_dataset_list(self) -> None:
        """Test serializing dataset for list view"""
        dataset = Dataset.objects.create(filename="test_list")
        EquipmentRecord.objects.create(
            dataset=dataset,
            equipment_name="Pump",
            type="Type",
            flowrate=100,
            pressure=50,
            temperature=25
        )
        
        serializer = DatasetListSerializer(dataset)
        data = serializer.data
        
        self.assertEqual(data['filename'], 'test_list')
        self.assertEqual(data['record_count'], 1)
        self.assertIn('id', data)
        self.assertIn('uploaded_at', data)


class DatasetDetailSerializerTests(TestCase):
    """Tests for DatasetDetailSerializer"""
    
    def test_serialize_dataset_detail(self) -> None:
        """Test serializing dataset with records"""
        dataset = Dataset.objects.create(filename="test_detail")
        EquipmentRecord.objects.create(
            dataset=dataset,
            equipment_name="Pump A",
            type="Centrifugal",
            flowrate=100,
            pressure=50,
            temperature=25
        )
        
        serializer = DatasetDetailSerializer(dataset)
        data = serializer.data
        
        self.assertEqual(data['filename'], 'test_detail')
        self.assertIn('records', data)
        self.assertEqual(len(data['records']), 1)
        self.assertEqual(data['records'][0]['equipment_name'], 'Pump A')


class SummarySerializerTests(TestCase):
    """Tests for SummarySerializer"""
    
    def test_serialize_summary(self) -> None:
        """Test serializing summary statistics"""
        summary_data = {
            'total_count': 100,
            'avg_flowrate': 150.5,
            'avg_pressure': 55.2,
            'avg_temperature': 27.5,
            'type_distribution': {'Pump': 60, 'Valve': 40}
        }
        
        serializer = SummarySerializer(summary_data)
        data = serializer.data
        
        self.assertEqual(data['total_count'], 100)
        self.assertEqual(data['avg_flowrate'], 150.5)
        self.assertEqual(data['type_distribution'], {'Pump': 60, 'Valve': 40})


class FileUploadSerializerTests(TestCase):
    """Tests for FileUploadSerializer"""
    
    def test_valid_csv_file(self) -> None:
        """Test validation with valid CSV file"""
        csv_file = SimpleUploadedFile(
            "test.csv",
            b"Equipment Name,Type,Flowrate,Pressure,Temperature\nTest,Pump,100,50,25",
            content_type="text/csv"
        )
        
        serializer = FileUploadSerializer(data={'file': csv_file})
        self.assertTrue(serializer.is_valid())
    
    def test_missing_file(self) -> None:
        """Test validation fails without file"""
        serializer = FileUploadSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertIn('file', serializer.errors)
    
    def test_optional_filename(self) -> None:
        """Test optional filename field"""
        csv_file = SimpleUploadedFile(
            "test.csv",
            b"Equipment Name,Type,Flowrate,Pressure,Temperature\nTest,Pump,100,50,25",
            content_type="text/csv"
        )
        
        serializer = FileUploadSerializer(
            data={'file': csv_file, 'filename': 'custom_name'}
        )
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['filename'], 'custom_name')


class UploadResponseSerializerTests(TestCase):
    """Tests for UploadResponseSerializer"""
    
    def test_serialize_success_response(self) -> None:
        """Test serializing successful upload response"""
        response_data = {
            'success': True,
            'dataset_id': 1,
            'message': 'Upload successful',
            'summary': {
                'total_count': 10,
                'avg_flowrate': 100.0,
                'avg_pressure': 50.0,
                'avg_temperature': 25.0,
                'type_distribution': {'Pump': 10}
            }
        }
        
        serializer = UploadResponseSerializer(response_data)
        data = serializer.data
        
        self.assertTrue(data['success'])
        self.assertEqual(data['dataset_id'], 1)
        self.assertIn('summary', data)


class ErrorResponseSerializerTests(TestCase):
    """Tests for ErrorResponseSerializer"""
    
    def test_serialize_error_response(self) -> None:
        """Test serializing error response"""
        error_data = {
            'error': 'Invalid file format',
            'details': ['File must be CSV', 'File size exceeds limit']
        }
        
        serializer = ErrorResponseSerializer(error_data)
        data = serializer.data
        
        self.assertEqual(data['error'], 'Invalid file format')
        self.assertEqual(len(data['details']), 2)
