"""
Unit Tests for API Services
Django 5 + Python 3.12 compatible
"""

from __future__ import annotations

import io
from decimal import Decimal
from unittest.mock import Mock, patch, MagicMock

import pandas as pd
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from api.services import (
    CSVValidationService,
    CSVProcessingService,
    StatisticsService,
)
from equipment.models import Dataset, EquipmentRecord


class CSVValidationServiceTests(TestCase):
    """Tests for CSV validation service"""
    
    def test_validate_file_accepts_csv(self) -> None:
        """Test that CSV files pass validation"""
        csv_file = SimpleUploadedFile(
            "test.csv",
            b"Equipment Name,Type,Flowrate,Pressure,Temperature\nTest,Pump,100,50,25",
            content_type="text/csv"
        )
        result = CSVValidationService.validate_file(csv_file)
        self.assertTrue(result['is_valid'])
    
    def test_validate_file_rejects_non_csv(self) -> None:
        """Test that non-CSV files are rejected"""
        txt_file = SimpleUploadedFile(
            "test.txt",
            b"This is not a CSV file",
            content_type="text/plain"
        )
        result = CSVValidationService.validate_file(txt_file)
        self.assertFalse(result['is_valid'])
        self.assertIn('CSV', result['errors'][0])
    
    def test_validate_file_rejects_empty(self) -> None:
        """Test that empty files are rejected"""
        empty_file = SimpleUploadedFile(
            "empty.csv",
            b"",
            content_type="text/csv"
        )
        result = CSVValidationService.validate_file(empty_file)
        self.assertFalse(result['is_valid'])
    
    def test_validate_file_rejects_large_file(self) -> None:
        """Test that files over 10MB are rejected"""
        large_content = b"x" * (11 * 1024 * 1024)  # 11MB
        large_file = SimpleUploadedFile(
            "large.csv",
            large_content,
            content_type="text/csv"
        )
        result = CSVValidationService.validate_file(large_file)
        self.assertFalse(result['is_valid'])
        self.assertIn('10MB', result['errors'][0])
    
    def test_validate_columns_success(self) -> None:
        """Test column validation with correct columns"""
        df = pd.DataFrame({
            'Equipment Name': ['Test'],
            'Type': ['Pump'],
            'Flowrate': [100.0],
            'Pressure': [50.0],
            'Temperature': [25.0]
        })
        result = CSVValidationService.validate_columns(df)
        self.assertTrue(result['is_valid'])
        self.assertEqual(len(result['errors']), 0)
    
    def test_validate_columns_missing(self) -> None:
        """Test validation fails with missing columns"""
        df = pd.DataFrame({
            'Equipment Name': ['Test'],
            'Type': ['Pump'],
            # Missing Flowrate, Pressure, Temperature
        })
        result = CSVValidationService.validate_columns(df)
        self.assertFalse(result['is_valid'])
        self.assertGreater(len(result['missing']), 0)
    
    def test_validate_columns_normalizes_names(self) -> None:
        """Test that column names are normalized"""
        df = pd.DataFrame({
            'equipment_name': ['Test'],  # underscore instead of space
            'Type': ['Pump'],
            'flow_rate': [100.0],  # underscore variant
            'Pressure': [50.0],
            'temp': [25.0]  # short form
        })
        result = CSVValidationService.validate_columns(df)
        self.assertTrue(result['is_valid'])
    
    def test_validate_data_types_success(self) -> None:
        """Test data type validation with valid data"""
        df = pd.DataFrame({
            'Equipment Name': ['Test'],
            'Type': ['Pump'],
            'Flowrate': [100.0],
            'Pressure': [50.0],
            'Temperature': [25.0]
        })
        result = CSVValidationService.validate_data_types(df)
        self.assertTrue(result['is_valid'])
    
    def test_validate_data_types_non_numeric(self) -> None:
        """Test validation fails with non-numeric values"""
        df = pd.DataFrame({
            'Equipment Name': ['Test'],
            'Type': ['Pump'],
            'Flowrate': ['not-a-number'],
            'Pressure': [50.0],
            'Temperature': [25.0]
        })
        result = CSVValidationService.validate_data_types(df)
        self.assertFalse(result['is_valid'])
    
    def test_validate_data_types_negative_values(self) -> None:
        """Test validation fails with negative values"""
        df = pd.DataFrame({
            'Equipment Name': ['Test'],
            'Type': ['Pump'],
            'Flowrate': [-100.0],  # Negative
            'Pressure': [50.0],
            'Temperature': [25.0]
        })
        result = CSVValidationService.validate_data_types(df)
        self.assertFalse(result['is_valid'])


class CSVProcessingServiceTests(TestCase):
    """Tests for CSV processing service"""
    
    def test_normalize_columns(self) -> None:
        """Test column normalization"""
        df = pd.DataFrame({
            'equipment_name': ['Test'],
            'type': ['Pump'],
            'flow_rate': [100.0],
            'press': [50.0],
            'temp': [25.0]
        })
        normalized = CSVProcessingService.normalize_columns(df)
        self.assertIn('Equipment Name', normalized.columns)
        self.assertIn('Type', normalized.columns)
        self.assertIn('Flowrate', normalized.columns)
        self.assertIn('Pressure', normalized.columns)
        self.assertIn('Temperature', normalized.columns)
    
    def test_process_file_success(self) -> None:
        """Test successful file processing"""
        csv_content = "Equipment Name,Type,Flowrate,Pressure,Temperature\n"
        csv_content += "Pump A,Centrifugal,100.5,50.2,25.0\n"
        csv_content += "Valve B,Gate,75.3,40.1,30.5\n"
        
        csv_file = SimpleUploadedFile(
            "test.csv",
            csv_content.encode('utf-8'),
            content_type="text/csv"
        )
        
        result = CSVProcessingService.process_file(csv_file)
        
        self.assertTrue(result['success'])
        self.assertIsNotNone(result['dataset_id'])
        self.assertIsNone(result['error'])
        
        # Verify dataset was created
        dataset = Dataset.objects.get(pk=result['dataset_id'])
        self.assertEqual(dataset.filename, "test")
        self.assertEqual(dataset.records.count(), 2)
    
    def test_process_file_invalid_columns(self) -> None:
        """Test file processing fails with invalid columns"""
        csv_content = "Name,Value\nTest,100\n"
        
        csv_file = SimpleUploadedFile(
            "invalid.csv",
            csv_content.encode('utf-8'),
            content_type="text/csv"
        )
        
        result = CSVProcessingService.process_file(csv_file)
        
        self.assertFalse(result['success'])
        self.assertIsNone(result['dataset_id'])
        self.assertIsNotNone(result['error'])
    
    def test_process_file_custom_filename(self) -> None:
        """Test processing with custom filename"""
        csv_content = "Equipment Name,Type,Flowrate,Pressure,Temperature\n"
        csv_content += "Pump A,Centrifugal,100.5,50.2,25.0\n"
        
        csv_file = SimpleUploadedFile(
            "original.csv",
            csv_content.encode('utf-8'),
            content_type="text/csv"
        )
        
        result = CSVProcessingService.process_file(csv_file, filename="custom_name")
        
        self.assertTrue(result['success'])
        dataset = Dataset.objects.get(pk=result['dataset_id'])
        self.assertEqual(dataset.filename, "custom_name")
    
    def test_process_file_keeps_last_5_datasets(self) -> None:
        """Test that only last 5 datasets are kept"""
        csv_content = "Equipment Name,Type,Flowrate,Pressure,Temperature\n"
        csv_content += "Pump,Type,100,50,25\n"
        
        # Create 6 datasets
        for i in range(6):
            csv_file = SimpleUploadedFile(
                f"test_{i}.csv",
                csv_content.encode('utf-8'),
                content_type="text/csv"
            )
            CSVProcessingService.process_file(csv_file)
        
        # Should only have 5 datasets
        self.assertEqual(Dataset.objects.count(), 5)


class StatisticsServiceTests(TestCase):
    """Tests for statistics calculation service"""
    
    def setUp(self) -> None:
        """Set up test data"""
        self.df = pd.DataFrame({
            'Equipment Name': ['A', 'B', 'C'],
            'Type': ['Pump', 'Pump', 'Valve'],
            'Flowrate': [100.0, 200.0, 150.0],
            'Pressure': [50.0, 60.0, 55.0],
            'Temperature': [25.0, 30.0, 27.5]
        })
    
    def test_calculate_from_dataframe(self) -> None:
        """Test statistics calculation from DataFrame"""
        stats = StatisticsService.calculate_from_dataframe(self.df)
        
        self.assertEqual(stats['total_count'], 3)
        self.assertEqual(stats['avg_flowrate'], 150.0)
        self.assertEqual(stats['avg_pressure'], 55.0)
        self.assertEqual(stats['avg_temperature'], 27.5)
        self.assertIn('Pump', stats['type_distribution'])
        self.assertEqual(stats['type_distribution']['Pump'], 2)
        self.assertEqual(stats['type_distribution']['Valve'], 1)
    
    def test_calculate_from_dataframe_empty(self) -> None:
        """Test statistics for empty DataFrame"""
        empty_df = pd.DataFrame(columns=['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'])
        stats = StatisticsService.calculate_from_dataframe(empty_df)
        
        self.assertEqual(stats['total_count'], 0)
        self.assertEqual(stats['avg_flowrate'], 0.0)
    
    def test_calculate_from_dataset(self) -> None:
        """Test statistics calculation from Dataset"""
        # Create dataset with records
        dataset = Dataset.objects.create(filename="test_stats")
        EquipmentRecord.objects.bulk_create([
            EquipmentRecord(
                dataset=dataset,
                equipment_name='Pump A',
                type='Centrifugal',
                flowrate=100.0,
                pressure=50.0,
                temperature=25.0
            ),
            EquipmentRecord(
                dataset=dataset,
                equipment_name='Pump B',
                type='Centrifugal',
                flowrate=200.0,
                pressure=60.0,
                temperature=30.0
            ),
        ])
        
        stats = StatisticsService.calculate_from_dataset(dataset.id)
        
        self.assertIsNotNone(stats)
        self.assertEqual(stats['total_count'], 2)
        self.assertEqual(stats['avg_flowrate'], 150.0)
    
    def test_calculate_from_dataset_not_found(self) -> None:
        """Test statistics for non-existent dataset"""
        stats = StatisticsService.calculate_from_dataset(99999)
        self.assertIsNone(stats)
    
    def test_get_extended_statistics(self) -> None:
        """Test extended statistics calculation"""
        stats = StatisticsService.get_extended_statistics(self.df)
        
        self.assertIn('flowrate', stats)
        self.assertIn('pressure', stats)
        self.assertIn('temperature', stats)
        
        # Check flowrate stats
        self.assertEqual(stats['flowrate']['min'], 100.0)
        self.assertEqual(stats['flowrate']['max'], 200.0)
        self.assertEqual(stats['flowrate']['mean'], 150.0)
        self.assertIn('std', stats['flowrate'])
