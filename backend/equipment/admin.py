"""
Django Admin Configuration for Equipment Models
"""

from django.contrib import admin
from django.http import HttpRequest
from .models import Dataset, EquipmentRecord


class EquipmentRecordInline(admin.TabularInline):
    model = EquipmentRecord
    extra = 0
    readonly_fields = ['equipment_name', 'type', 'flowrate', 'pressure', 'temperature']
    can_delete = False
    
    def has_add_permission(self, request: HttpRequest, obj=None) -> bool:
        return False


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ['filename', 'uploaded_at', 'record_count', 'get_avg_flowrate']
    list_filter = ['uploaded_at']
    search_fields = ['filename']
    readonly_fields = ['uploaded_at', 'summary_json', 'record_count']
    inlines = [EquipmentRecordInline]
    
    @admin.display(description='Records')
    def record_count(self, obj: Dataset) -> int:
        return obj.record_count
    
    @admin.display(description='Avg Flowrate')
    def get_avg_flowrate(self, obj: Dataset) -> str:
        summary = obj.summary_json or {}
        avg = summary.get('avg_flowrate', 0)
        return f"{avg:.2f}" if avg else "-"


@admin.register(EquipmentRecord)
class EquipmentRecordAdmin(admin.ModelAdmin):
    list_display = ['equipment_name', 'type', 'flowrate', 'pressure', 'temperature', 'dataset']
    list_filter = ['type', 'dataset']
    search_fields = ['equipment_name']

