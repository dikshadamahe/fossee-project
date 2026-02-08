#!/usr/bin/env python
"""
Sample CSV Loader Script
Loads sample CSV data into the Django database
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import pandas as pd
from django.contrib.auth.models import User
from equipment.models import Dataset, EquipmentRecord


def load_sample_csv(file_path: str, user: User, name: str = None):
    """Load a CSV file into the database"""
    
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return None
    
    print(f"Loading CSV: {file_path}")
    
    # Read CSV
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()
    
    # Normalize column names
    column_mapping = {
        'equipment name': 'Equipment Name',
        'equipment_name': 'Equipment Name',
        'type': 'Type',
        'equipment_type': 'Type',
        'flowrate': 'Flowrate',
        'flow_rate': 'Flowrate',
        'pressure': 'Pressure',
        'temperature': 'Temperature',
        'temp': 'Temperature',
    }
    
    for old, new in column_mapping.items():
        for col in df.columns:
            if col.lower() == old:
                df.rename(columns={col: new}, inplace=True)
    
    # Validate columns
    required = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
    missing = [col for col in required if col not in df.columns]
    
    if missing:
        print(f"Error: Missing columns: {missing}")
        return None
    
    # Convert numeric columns
    for col in ['Flowrate', 'Pressure', 'Temperature']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Calculate statistics
    statistics = {
        'flowrate': {
            'min': float(df['Flowrate'].min()),
            'max': float(df['Flowrate'].max()),
            'mean': float(df['Flowrate'].mean()),
            'std': float(df['Flowrate'].std()) if len(df) > 1 else 0,
        },
        'pressure': {
            'min': float(df['Pressure'].min()),
            'max': float(df['Pressure'].max()),
            'mean': float(df['Pressure'].mean()),
            'std': float(df['Pressure'].std()) if len(df) > 1 else 0,
        },
        'temperature': {
            'min': float(df['Temperature'].min()),
            'max': float(df['Temperature'].max()),
            'mean': float(df['Temperature'].mean()),
            'std': float(df['Temperature'].std()) if len(df) > 1 else 0,
        },
        'type_distribution': df['Type'].value_counts().to_dict(),
    }
    
    # Create dataset
    if name is None:
        name = os.path.basename(file_path).replace('.csv', '')
    
    dataset = Dataset.objects.create(
        name=name,
        user=user,
        row_count=len(df),
        is_valid=True,
        statistics=statistics
    )
    
    # Create records
    records = []
    for _, row in df.iterrows():
        records.append(EquipmentRecord(
            dataset=dataset,
            equipment_name=str(row['Equipment Name']),
            equipment_type=str(row['Type']),
            flowrate=float(row['Flowrate']),
            pressure=float(row['Pressure']),
            temperature=float(row['Temperature'])
        ))
    
    EquipmentRecord.objects.bulk_create(records)
    
    print(f"Successfully loaded {len(records)} records into dataset '{name}'")
    return dataset


def main():
    """Main function"""
    
    # Get or create admin user
    try:
        user = User.objects.get(username='admin')
        print(f"Using existing user: admin")
    except User.DoesNotExist:
        user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print(f"Created admin user (password: admin123)")
    
    # Load sample CSV
    sample_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'equipment_sample.csv')
    
    if os.path.exists(sample_path):
        load_sample_csv(sample_path, user, "Sample Equipment Data")
    else:
        print(f"Sample CSV not found at: {sample_path}")
        print("You can create your own CSV with these columns:")
        print("Equipment Name, Type, Flowrate, Pressure, Temperature")


if __name__ == '__main__':
    main()
