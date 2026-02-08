# Generated migration for equipment models
# Updated for new model structure - Python 3.12 / Django 5

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=255, help_text='Name of the uploaded CSV file')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('csv_file', models.FileField(upload_to='datasets/', blank=True, null=True)),
                ('summary_json', models.JSONField(blank=True, null=True, help_text='Calculated statistics in JSON format')),
            ],
            options={
                'ordering': ['-uploaded_at'],
                'verbose_name': 'Dataset',
                'verbose_name_plural': 'Datasets',
            },
        ),
        migrations.CreateModel(
            name='EquipmentRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equipment_name', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=100, help_text='Equipment type (e.g., Pump, Valve)')),
                ('flowrate', models.FloatField()),
                ('pressure', models.FloatField()),
                ('temperature', models.FloatField()),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='equipment.dataset')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Equipment Record',
                'verbose_name_plural': 'Equipment Records',
            },
        ),
    ]
