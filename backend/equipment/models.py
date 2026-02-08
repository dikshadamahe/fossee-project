"""
Django Models for Chemical Equipment Parameter Visualizer
Python 3.12 compatible with full type hints
"""

from __future__ import annotations

from typing import Any
from django.db import models
from django.conf import settings


class Dataset(models.Model):
    """
    Model for storing uploaded CSV datasets.
    Automatically maintains only the last 5 datasets.
    """
    
    id: int
    uploaded_at = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=255)
    summary_json = models.JSONField(default=dict, blank=True)
    csv_file = models.FileField(upload_to='datasets/', null=True, blank=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Dataset'
        verbose_name_plural = 'Datasets'
    
    def __str__(self) -> str:
        return f"{self.filename} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"
    
    def save(self, *args: Any, **kwargs: Any) -> None:
        super().save(*args, **kwargs)
        self._cleanup_old_datasets()
    
    def _cleanup_old_datasets(self) -> None:
        """Keep only last 5 datasets globally"""
        max_datasets: int = getattr(settings, 'MAX_DATASETS', 5)
        all_datasets = Dataset.objects.order_by('-uploaded_at')
        
        if all_datasets.count() > max_datasets:
            datasets_to_delete = all_datasets[max_datasets:]
            for dataset in datasets_to_delete:
                if dataset.csv_file:
                    dataset.csv_file.delete(save=False)
                dataset.delete()
    
    @property
    def record_count(self) -> int:
        """Get count of equipment records"""
        return self.records.count()


class EquipmentRecord(models.Model):
    """Model for individual equipment records from CSV"""
    
    id: int
    dataset = models.ForeignKey(
        Dataset,
        on_delete=models.CASCADE,
        related_name='records'
    )
    equipment_name = models.CharField(max_length=255)
    type = models.CharField(max_length=100)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Equipment Record'
        verbose_name_plural = 'Equipment Records'
    
    def __str__(self) -> str:
        return f"{self.equipment_name} ({self.type})"
