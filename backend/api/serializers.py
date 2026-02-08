"""
Django REST Framework Serializers
Python 3.12 compatible with type hints
"""

from __future__ import annotations

from typing import Any
from rest_framework import serializers
from equipment.models import Dataset, EquipmentRecord


class EquipmentRecordSerializer(serializers.ModelSerializer):
    """Serializer for equipment records"""
    
    class Meta:
        model = EquipmentRecord
        fields: list[str] = [
            'id',
            'equipment_name',
            'type',
            'flowrate',
            'pressure',
            'temperature'
        ]
        read_only_fields: list[str] = ['id']


class DatasetListSerializer(serializers.ModelSerializer):
    """Serializer for dataset list view"""
    
    record_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Dataset
        fields: list[str] = [
            'id',
            'filename',
            'uploaded_at',
            'record_count'
        ]
        read_only_fields: list[str] = ['id', 'uploaded_at', 'record_count']


class DatasetDetailSerializer(serializers.ModelSerializer):
    """Serializer for dataset detail view with records"""
    
    records = EquipmentRecordSerializer(many=True, read_only=True)
    record_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Dataset
        fields: list[str] = [
            'id',
            'filename',
            'uploaded_at',
            'record_count',
            'summary_json',
            'records'
        ]
        read_only_fields: list[str] = ['id', 'uploaded_at', 'summary_json', 'record_count']


class SummarySerializer(serializers.Serializer):
    """Serializer for dataset summary/statistics"""
    
    total_count = serializers.IntegerField()
    avg_flowrate = serializers.FloatField()
    avg_pressure = serializers.FloatField()
    avg_temperature = serializers.FloatField()
    type_distribution = serializers.DictField(
        child=serializers.IntegerField()
    )


class ExtendedStatisticsSerializer(serializers.Serializer):
    """Serializer for extended statistics with min/max/std"""
    
    class ParameterStatsSerializer(serializers.Serializer):
        min = serializers.FloatField()
        max = serializers.FloatField()
        mean = serializers.FloatField()
        std = serializers.FloatField()
        median = serializers.FloatField()
    
    total_count = serializers.IntegerField()
    parameters = serializers.DictField(
        child=ParameterStatsSerializer()
    )
    type_distribution = serializers.DictField(
        child=serializers.IntegerField()
    )


class FileUploadSerializer(serializers.Serializer):
    """Serializer for CSV file upload"""
    
    file = serializers.FileField(
        help_text="CSV file with columns: Equipment Name, Type, Flowrate, Pressure, Temperature"
    )
    filename = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        help_text="Optional custom filename for the dataset"
    )
    
    def validate_file(self, value: Any) -> Any:
        """Validate file is CSV"""
        if not value.name.lower().endswith('.csv'):
            raise serializers.ValidationError("Only CSV files are allowed.")
        
        # Check file size (max 10MB)
        max_size = 10 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError(
                f"File too large. Maximum size is 10MB."
            )
        
        return value


class UploadResponseSerializer(serializers.Serializer):
    """Serializer for upload response"""
    
    success = serializers.BooleanField()
    dataset_id = serializers.IntegerField(allow_null=True)
    message = serializers.CharField()
    summary = SummarySerializer(required=False, allow_null=True)


class ErrorResponseSerializer(serializers.Serializer):
    """Serializer for error responses"""
    
    error = serializers.CharField()
    details = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
