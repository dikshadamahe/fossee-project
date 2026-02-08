"""
Unit Tests for Analytics Service
Python 3.12 compatible
"""

from __future__ import annotations

import pandas as pd
import numpy as np
from django.test import TestCase

from api.analytics import (
    AnalyticsService,
    AnalyticsConfig,
    HealthStatus,
)


class AnalyticsServiceTests(TestCase):
    """Tests for AnalyticsService"""
    
    def setUp(self) -> None:
        """Set up test data"""
        self.service = AnalyticsService()
        self.sample_df = pd.DataFrame({
            'Equipment Name': ['Pump A', 'Pump B', 'Valve C', 'Compressor D', 'Pump E'],
            'Type': ['Centrifugal', 'Centrifugal', 'Gate', 'Reciprocating', 'Centrifugal'],
            'Flowrate': [100.0, 150.0, 75.0, 200.0, 125.0],
            'Pressure': [50.0, 55.0, 40.0, 70.0, 52.0],
            'Temperature': [25.0, 30.0, 22.0, 35.0, 28.0]
        })
    
    def test_calculate_parameter_stats(self) -> None:
        """Test parameter statistics calculation"""
        stats = AnalyticsService.calculate_parameter_stats(self.sample_df)
        
        self.assertIn('flowrate', stats)
        self.assertIn('pressure', stats)
        self.assertIn('temperature', stats)
        
        # Check flowrate stats
        flowrate = stats['flowrate']
        self.assertEqual(flowrate['min'], 75.0)
        self.assertEqual(flowrate['max'], 200.0)
        self.assertEqual(flowrate['mean'], 130.0)
        self.assertIn('std', flowrate)
        self.assertIn('q1', flowrate)
        self.assertIn('q3', flowrate)
        self.assertIn('iqr', flowrate)
    
    def test_calculate_parameter_stats_empty_df(self) -> None:
        """Test stats calculation with empty DataFrame"""
        empty_df = pd.DataFrame(columns=['Flowrate', 'Pressure', 'Temperature'])
        stats = AnalyticsService.calculate_parameter_stats(empty_df)
        
        self.assertEqual(stats['flowrate']['min'], 0.0)
        self.assertEqual(stats['flowrate']['mean'], 0.0)
    
    def test_calculate_type_distribution(self) -> None:
        """Test equipment type distribution calculation"""
        distribution = AnalyticsService.calculate_type_distribution(self.sample_df)
        
        self.assertEqual(len(distribution), 3)  # 3 unique types
        
        # Centrifugal should be most common
        self.assertEqual(distribution[0]['type'], 'Centrifugal')
        self.assertEqual(distribution[0]['count'], 3)
        self.assertEqual(distribution[0]['percentage'], 60.0)
    
    def test_calculate_type_distribution_empty(self) -> None:
        """Test distribution with empty DataFrame"""
        empty_df = pd.DataFrame(columns=['Type'])
        distribution = AnalyticsService.calculate_type_distribution(empty_df)
        
        self.assertEqual(len(distribution), 0)
    
    def test_detect_outliers(self) -> None:
        """Test outlier detection using IQR method"""
        # Add an outlier
        df_with_outlier = self.sample_df.copy()
        df_with_outlier.loc[5] = ['Outlier F', 'Pump', 500.0, 50.0, 25.0]  # Extreme flowrate
        
        outliers = self.service.detect_outliers(df_with_outlier)
        
        # Should detect the flowrate outlier
        flowrate_outliers = [o for o in outliers if o['parameter'] == 'flowrate']
        self.assertGreater(len(flowrate_outliers), 0)
        self.assertEqual(flowrate_outliers[0]['equipment_name'], 'Outlier F')
        self.assertEqual(flowrate_outliers[0]['deviation_type'], 'high')
    
    def test_detect_outliers_no_outliers(self) -> None:
        """Test outlier detection with no outliers"""
        outliers = self.service.detect_outliers(self.sample_df)
        
        # Sample data shouldn't have extreme outliers
        self.assertEqual(len(outliers), 0)
    
    def test_detect_outliers_custom_multiplier(self) -> None:
        """Test outlier detection with custom IQR multiplier"""
        # Lower multiplier = more sensitive to outliers
        outliers_strict = self.service.detect_outliers(self.sample_df, iqr_multiplier=0.5)
        outliers_lenient = self.service.detect_outliers(self.sample_df, iqr_multiplier=3.0)
        
        # Stricter should find more outliers
        self.assertGreaterEqual(len(outliers_strict), len(outliers_lenient))
    
    def test_calculate_health_score(self) -> None:
        """Test health score calculation"""
        health_scores = self.service.calculate_health_score(self.sample_df)
        
        self.assertEqual(len(health_scores), 5)
        
        for score in health_scores:
            self.assertIn('equipment_name', score)
            self.assertIn('health_score', score)
            self.assertIn('status', score)
            self.assertIn('factors', score)
            
            # Score should be 0-100
            self.assertGreaterEqual(score['health_score'], 0)
            self.assertLessEqual(score['health_score'], 100)
    
    def test_calculate_health_score_custom_ranges(self) -> None:
        """Test health score with custom optimal ranges"""
        custom_ranges = {
            'flowrate': (90.0, 160.0),
            'pressure': (45.0, 60.0),
            'temperature': (20.0, 35.0)
        }
        
        health_scores = self.service.calculate_health_score(
            self.sample_df, 
            optimal_ranges=custom_ranges
        )
        
        # All values in sample should be within these ranges
        for score in health_scores:
            self.assertGreater(score['health_score'], 50)
    
    def test_health_status_mapping(self) -> None:
        """Test health score to status mapping"""
        self.assertEqual(
            AnalyticsService._get_health_status(95), 
            HealthStatus.EXCELLENT
        )
        self.assertEqual(
            AnalyticsService._get_health_status(80), 
            HealthStatus.GOOD
        )
        self.assertEqual(
            AnalyticsService._get_health_status(60), 
            HealthStatus.FAIR
        )
        self.assertEqual(
            AnalyticsService._get_health_status(30), 
            HealthStatus.POOR
        )
        self.assertEqual(
            AnalyticsService._get_health_status(10), 
            HealthStatus.CRITICAL
        )
    
    def test_parameter_score_within_range(self) -> None:
        """Test parameter score when value is within optimal range"""
        score = AnalyticsService._calculate_parameter_score(
            value=100.0, 
            optimal_min=50.0, 
            optimal_max=150.0
        )
        self.assertEqual(score, 100.0)
    
    def test_parameter_score_outside_range(self) -> None:
        """Test parameter score when value is outside optimal range"""
        score = AnalyticsService._calculate_parameter_score(
            value=200.0, 
            optimal_min=50.0, 
            optimal_max=100.0
        )
        self.assertLess(score, 100.0)
        self.assertGreater(score, 0.0)
    
    def test_analyze_complete(self) -> None:
        """Test complete analytics analysis"""
        result = self.service.analyze(self.sample_df)
        
        self.assertIn('parameter_stats', result)
        self.assertIn('type_distribution', result)
        self.assertIn('outliers', result)
        self.assertIn('health_scores', result)
        self.assertIn('summary', result)
        
        # Check summary
        summary = result['summary']
        self.assertEqual(summary['total_records'], 5)
        self.assertEqual(summary['equipment_types_count'], 3)
        self.assertIn('average_health_score', summary)
    
    def test_from_records(self) -> None:
        """Test analytics from list of record dictionaries"""
        records = [
            {'equipment_name': 'Pump A', 'type': 'Centrifugal', 
             'flowrate': 100.0, 'pressure': 50.0, 'temperature': 25.0},
            {'equipment_name': 'Valve B', 'type': 'Gate', 
             'flowrate': 80.0, 'pressure': 45.0, 'temperature': 22.0},
        ]
        
        result = AnalyticsService.from_records(records)
        
        self.assertEqual(result['summary']['total_records'], 2)
        self.assertEqual(len(result['health_scores']), 2)
    
    def test_normalize_columns(self) -> None:
        """Test column name normalization"""
        df = pd.DataFrame({
            'equipment_name': ['Pump A'],
            'type': ['Centrifugal'],
            'flow_rate': [100.0],
            'pressure': [50.0],
            'temp': [25.0]
        })
        
        normalized = AnalyticsService._normalize_columns(df)
        
        self.assertIn('Equipment Name', normalized.columns)
        self.assertIn('Flowrate', normalized.columns)
        self.assertIn('Temperature', normalized.columns)


class AnalyticsConfigTests(TestCase):
    """Tests for AnalyticsConfig"""
    
    def test_default_config(self) -> None:
        """Test default configuration values"""
        config = AnalyticsConfig()
        
        self.assertEqual(config.iqr_multiplier, 1.5)
        self.assertIn('flowrate', config.health_weights)
        self.assertIn('pressure', config.health_weights)
        self.assertIn('temperature', config.health_weights)
    
    def test_custom_config(self) -> None:
        """Test custom configuration"""
        config = AnalyticsConfig(
            iqr_multiplier=2.0,
            health_weights={'flowrate': 0.5, 'pressure': 0.3, 'temperature': 0.2}
        )
        
        self.assertEqual(config.iqr_multiplier, 2.0)
        self.assertEqual(config.health_weights['flowrate'], 0.5)
    
    def test_service_with_custom_config(self) -> None:
        """Test service uses custom configuration"""
        config = AnalyticsConfig(iqr_multiplier=3.0)
        service = AnalyticsService(config)
        
        self.assertEqual(service.config.iqr_multiplier, 3.0)
