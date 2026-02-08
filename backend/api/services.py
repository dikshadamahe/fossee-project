"""
Services Layer for Chemical Equipment Parameter Visualizer
Business logic separated from views - Python 3.12 compatible
"""

from __future__ import annotations

import io
from typing import TypedDict, Any
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from django.core.files.uploadedfile import UploadedFile
from django.db.models import Avg, Count

from equipment.models import Dataset, EquipmentRecord


# Type definitions
class StatisticsDict(TypedDict):
    total_count: int
    avg_flowrate: float
    avg_pressure: float
    avg_temperature: float
    type_distribution: dict[str, int]


class ValidationResult(TypedDict):
    valid: bool
    errors: list[str]
    warnings: list[str]


class UploadResult(TypedDict):
    success: bool
    dataset_id: int | None
    error: str | None


# Required CSV columns (internal names)
REQUIRED_COLUMNS: tuple[str, ...] = (
    'Equipment Name',
    'Type', 
    'Flowrate',
    'Pressure',
    'Temperature'
)

# Column name mappings for flexible parsing (all lowercase for matching)
COLUMN_MAPPING: dict[str, str] = {
    # Equipment Name variations
    'equipment_name': 'Equipment Name',
    'equipment name': 'Equipment Name',
    'equipmentname': 'Equipment Name',
    'name': 'Equipment Name',
    'equipment': 'Equipment Name',
    'equip_name': 'Equipment Name',
    'equip name': 'Equipment Name',
    'equipname': 'Equipment Name',
    'device': 'Equipment Name',
    'device_name': 'Equipment Name',
    'device name': 'Equipment Name',
    'asset': 'Equipment Name',
    'asset_name': 'Equipment Name',
    'id': 'Equipment Name',
    'equipment_id': 'Equipment Name',
    'equip_id': 'Equipment Name',
    
    # Type variations
    'type': 'Type',
    'equipment_type': 'Type',
    'equipment type': 'Type',
    'equipmenttype': 'Type',
    'category': 'Type',
    'equip_type': 'Type',
    'device_type': 'Type',
    'asset_type': 'Type',
    'class': 'Type',
    'classification': 'Type',
    'kind': 'Type',
    
    # Flowrate variations
    'flowrate': 'Flowrate',
    'flow_rate': 'Flowrate',
    'flow rate': 'Flowrate',
    'flow-rate': 'Flowrate',
    'flow': 'Flowrate',
    'flowrt': 'Flowrate',
    'flow_rt': 'Flowrate',
    'rate': 'Flowrate',
    'flow_speed': 'Flowrate',
    'flowspeed': 'Flowrate',
    'volumetric_flow': 'Flowrate',
    'volume_flow': 'Flowrate',
    'discharge': 'Flowrate',
    'discharge_rate': 'Flowrate',
    'q': 'Flowrate',  # Common engineering symbol
    
    # Pressure variations
    'pressure': 'Pressure',
    'press': 'Pressure',
    'pres': 'Pressure',
    'psi': 'Pressure',
    'bar': 'Pressure',
    'kpa': 'Pressure',
    'mpa': 'Pressure',
    'pressure_reading': 'Pressure',
    'static_pressure': 'Pressure',
    'dynamic_pressure': 'Pressure',
    'p': 'Pressure',  # Common engineering symbol
    'press_value': 'Pressure',
    
    # Temperature variations
    'temperature': 'Temperature',
    'temp': 'Temperature',
    'tmp': 'Temperature',
    'celsius': 'Temperature',
    'fahrenheit': 'Temperature',
    'kelvin': 'Temperature',
    'deg': 'Temperature',
    'degree': 'Temperature',
    'degrees': 'Temperature',
    'temp_reading': 'Temperature',
    'temperature_reading': 'Temperature',
    't': 'Temperature',  # Common engineering symbol
    'thermal': 'Temperature',
    'heat': 'Temperature',
}


@dataclass
class CSVValidationService:
    """Service for validating CSV file structure and content"""
    
    @staticmethod
    def validate_file(file: UploadedFile) -> ValidationResult:
        """Validate uploaded CSV file"""
        errors: list[str] = []
        warnings: list[str] = []
        
        # Check file extension
        filename = file.name or ''
        if not filename.lower().endswith('.csv'):
            errors.append("File must be a CSV file (.csv extension)")
            return ValidationResult(valid=False, errors=errors, warnings=warnings)
        
        # Check file size (max 10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        if file.size and file.size > max_size:
            errors.append(f"File too large. Maximum size is 10MB, got {file.size / 1024 / 1024:.1f}MB")
            return ValidationResult(valid=False, errors=errors, warnings=warnings)
        
        try:
            # Read file content
            content = file.read().decode('utf-8')
            file.seek(0)  # Reset file pointer
            
            # Parse CSV
            df = pd.read_csv(io.StringIO(content))
            
            if df.empty:
                errors.append("CSV file is empty")
                return ValidationResult(valid=False, errors=errors, warnings=warnings)
            
            # Validate columns
            column_validation = CSVValidationService._validate_columns(df)
            errors.extend(column_validation['errors'])
            warnings.extend(column_validation['warnings'])
            
            if errors:
                return ValidationResult(valid=False, errors=errors, warnings=warnings)
            
            # Validate data types
            data_validation = CSVValidationService._validate_data_types(df)
            errors.extend(data_validation['errors'])
            warnings.extend(data_validation['warnings'])
            
        except pd.errors.EmptyDataError:
            errors.append("CSV file is empty or malformed")
        except UnicodeDecodeError:
            errors.append("File encoding not supported. Please use UTF-8 encoding")
        except Exception as e:
            errors.append(f"Failed to parse CSV: {str(e)}")
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    @staticmethod
    def _validate_columns(df: pd.DataFrame) -> dict[str, list[str]]:
        """Validate that required columns are present"""
        errors: list[str] = []
        warnings: list[str] = []
        
        # Normalize column names
        df.columns = df.columns.str.strip()
        found_columns: set[str] = set()
        
        for col in df.columns:
            col_lower = col.lower().strip()
            if col_lower in COLUMN_MAPPING:
                found_columns.add(COLUMN_MAPPING[col_lower])
            elif col in REQUIRED_COLUMNS:
                found_columns.add(col)
        
        # Check for missing columns
        missing = set(REQUIRED_COLUMNS) - found_columns
        if missing:
            # Build helpful error message
            actual_cols = list(df.columns)
            
            # Get example accepted names for each missing column
            hints: list[str] = []
            for m in sorted(missing):
                examples = [k for k, v in COLUMN_MAPPING.items() if v == m][:3]
                hints.append(f'"{m}" (accepts: {", ".join(examples)}...)')
            
            errors.append(
                f"Missing {len(missing)} required column(s):\n"
                f"  • {chr(10).join('• ' + h for h in hints)}\n"
                f"Your CSV has these columns: {', '.join(actual_cols)}"
            )
        
        return {'errors': errors, 'warnings': warnings}
    
    @staticmethod
    def _validate_data_types(df: pd.DataFrame) -> dict[str, list[str]]:
        """Validate data types in the dataframe"""
        errors: list[str] = []
        warnings: list[str] = []
        
        # Normalize columns first
        df = CSVProcessingService.normalize_columns(df)
        
        numeric_columns = ['Flowrate', 'Pressure', 'Temperature']
        
        for col in numeric_columns:
            if col in df.columns:
                # Try to convert to numeric
                numeric_series = pd.to_numeric(df[col], errors='coerce')
                invalid_count = numeric_series.isna().sum() - df[col].isna().sum()
                
                if invalid_count > 0:
                    errors.append(f"Column '{col}' contains {invalid_count} non-numeric values")
                
                # Check for negative values
                if (numeric_series < 0).any():
                    warnings.append(f"Column '{col}' contains negative values")
        
        return {'errors': errors, 'warnings': warnings}


class CSVProcessingService:
    """Service for processing CSV files and creating datasets"""
    
    @staticmethod
    def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Normalize column names to standard format"""
        df = df.copy()
        df.columns = df.columns.str.strip()
        
        column_renames: dict[str, str] = {}
        for col in df.columns:
            col_lower = col.lower().strip()
            if col_lower in COLUMN_MAPPING:
                column_renames[col] = COLUMN_MAPPING[col_lower]
            elif col in REQUIRED_COLUMNS:
                column_renames[col] = col
        
        df.rename(columns=column_renames, inplace=True)
        return df
    
    @staticmethod
    def process_file(
        file: UploadedFile, 
        filename: str | None = None,
        user: Any = None
    ) -> UploadResult:
        """Process uploaded CSV file and create dataset.
        
        Args:
            file: The uploaded CSV file
            filename: Optional custom filename
            user: Optional user for dataset ownership (None for anonymous)
        """
        
        # Validate first
        validation = CSVValidationService.validate_file(file)
        if not validation['valid']:
            return UploadResult(
                success=False,
                dataset_id=None,
                error='; '.join(validation['errors'])
            )
        
        try:
            # Read and process CSV
            content = file.read().decode('utf-8')
            file.seek(0)
            
            df = pd.read_csv(io.StringIO(content))
            df = CSVProcessingService.normalize_columns(df)
            
            # Convert numeric columns
            for col in ['Flowrate', 'Pressure', 'Temperature']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Drop rows with NaN values in required columns
            df = df.dropna(subset=REQUIRED_COLUMNS)
            
            # Calculate summary statistics
            summary = StatisticsService.calculate_from_dataframe(df)
            
            # Determine filename
            if filename is None:
                filename = Path(file.name or 'uploaded.csv').stem
            
            # Create dataset with user ownership
            dataset = Dataset.objects.create(
                filename=filename,
                summary_json=summary,
                csv_file=file,
                user=user  # Associate with user (None for anonymous)
            )
            
            # Create equipment records
            records: list[EquipmentRecord] = []
            for _, row in df.iterrows():
                records.append(EquipmentRecord(
                    dataset=dataset,
                    equipment_name=str(row['Equipment Name']),
                    type=str(row['Type']),
                    flowrate=float(row['Flowrate']),
                    pressure=float(row['Pressure']),
                    temperature=float(row['Temperature'])
                ))
            
            EquipmentRecord.objects.bulk_create(records)
            
            return UploadResult(
                success=True,
                dataset_id=dataset.id,
                error=None
            )
            
        except Exception as e:
            return UploadResult(
                success=False,
                dataset_id=None,
                error=f"Failed to process file: {str(e)}"
            )


class StatisticsService:
    """Service for calculating dataset statistics"""
    
    @staticmethod
    def calculate_from_dataframe(df: pd.DataFrame) -> StatisticsDict:
        """Calculate statistics from a pandas DataFrame"""
        
        type_distribution = df['Type'].value_counts().to_dict()
        
        return StatisticsDict(
            total_count=len(df),
            avg_flowrate=round(float(df['Flowrate'].mean()), 4) if len(df) > 0 else 0.0,
            avg_pressure=round(float(df['Pressure'].mean()), 4) if len(df) > 0 else 0.0,
            avg_temperature=round(float(df['Temperature'].mean()), 4) if len(df) > 0 else 0.0,
            type_distribution=type_distribution
        )
    
    @staticmethod
    def calculate_from_dataset(dataset_id: int) -> StatisticsDict | None:
        """Calculate statistics from database records"""
        
        try:
            dataset = Dataset.objects.get(pk=dataset_id)
        except Dataset.DoesNotExist:
            return None
        
        records = dataset.records.all()
        
        if not records.exists():
            return StatisticsDict(
                total_count=0,
                avg_flowrate=0.0,
                avg_pressure=0.0,
                avg_temperature=0.0,
                type_distribution={}
            )
        
        # Calculate averages using Django ORM
        aggregates = records.aggregate(
            avg_flowrate=Avg('flowrate'),
            avg_pressure=Avg('pressure'),
            avg_temperature=Avg('temperature')
        )
        
        # Calculate type distribution
        type_counts = records.values('type').annotate(count=Count('id'))
        type_distribution = {item['type']: item['count'] for item in type_counts}
        
        return StatisticsDict(
            total_count=records.count(),
            avg_flowrate=round(aggregates['avg_flowrate'] or 0.0, 4),
            avg_pressure=round(aggregates['avg_pressure'] or 0.0, 4),
            avg_temperature=round(aggregates['avg_temperature'] or 0.0, 4),
            type_distribution=type_distribution
        )
    
    @staticmethod
    def get_extended_statistics(dataset_id: int) -> dict[str, Any] | None:
        """Get extended statistics including min, max, std for each parameter"""
        
        try:
            dataset = Dataset.objects.get(pk=dataset_id)
        except Dataset.DoesNotExist:
            return None
        
        records = dataset.records.all()
        
        if not records.exists():
            return None
        
        # Convert to DataFrame for easier calculation
        data = list(records.values('flowrate', 'pressure', 'temperature', 'type'))
        df = pd.DataFrame(data)
        
        result: dict[str, Any] = {
            'total_count': len(df),
            'parameters': {}
        }
        
        for param in ['flowrate', 'pressure', 'temperature']:
            result['parameters'][param] = {
                'min': round(float(df[param].min()), 4),
                'max': round(float(df[param].max()), 4),
                'mean': round(float(df[param].mean()), 4),
                'std': round(float(df[param].std()), 4) if len(df) > 1 else 0.0,
                'median': round(float(df[param].median()), 4),
            }
        
        result['type_distribution'] = df['type'].value_counts().to_dict()
        
        return result
