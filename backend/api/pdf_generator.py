"""
PDF Report Generator for Chemical Equipment Parameter Visualizer
Following FOSSEE Scientific Analytics UI design system

Design Spec (design.md Section 12):
- Serif headings (Times-Roman)
- Mono tables (Courier)
- FOSSEE colors
- Charts as vector/images

Django 5 + Python 3.12 compatible
"""

from __future__ import annotations

import io
import json
from datetime import datetime
from typing import TYPE_CHECKING, Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    Image, KeepTogether, HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics import renderPDF

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

if TYPE_CHECKING:
    from equipment.models import Dataset


# =============================================================================
# FOSSEE Design Tokens (from design.md)
# =============================================================================

COLORS = {
    # Brand Palette
    'primary_900': colors.HexColor('#0F2A44'),  # Headers, nav
    'primary_700': colors.HexColor('#1B7F79'),  # Primary actions
    'primary_600': colors.HexColor('#3A4E9F'),  # Analytics highlight
    'success': colors.HexColor('#2EA043'),       # Valid, positive
    'warning': colors.HexColor('#D97706'),       # Data issues
    'error': colors.HexColor('#C53030'),         # Validation error
    
    # Neutrals
    'bg_main': colors.HexColor('#F7F9FC'),       # Background
    'surface': colors.HexColor('#FFFFFF'),       # Cards
    'border': colors.HexColor('#E2E8F0'),        # Dividers
    'text_primary': colors.HexColor('#102A43'),  # Body text
    'text_secondary': colors.HexColor('#486581'),# Subtext
    'text_muted': colors.HexColor('#829AB1'),    # Labels
    
    # Chart Palette
    'flowrate': colors.HexColor('#1B7F79'),
    'pressure': colors.HexColor('#3A4E9F'),
    'temperature': colors.HexColor('#C53030'),
    'chart_4': colors.HexColor('#D97706'),
}

# Chart color hex values for matplotlib
CHART_COLORS_HEX = {
    'flowrate': '#1B7F79',
    'pressure': '#3A4E9F', 
    'temperature': '#C53030',
    'distribution': ['#1B7F79', '#3A4E9F', '#2EA043', '#D97706'],
}

# Typography (design.md Section 3)
FONTS = {
    'heading': 'Times-Roman',      # Serif for headings (PDF report style)
    'heading_bold': 'Times-Bold',
    'body': 'Helvetica',           # Sans-serif body
    'mono': 'Courier',             # Mono for tables & numbers
    'mono_bold': 'Courier-Bold',
}

# Size scale (design.md Section 3.2)
FONT_SIZES = {
    'h1': 28,
    'h2': 22,
    'h3': 18,
    'body': 15,
    'small': 13,
    'mono': 13,
}


# =============================================================================
# Chart Generation (Matplotlib)
# =============================================================================

def create_parameter_charts(dataset: Dataset) -> io.BytesIO:
    """
    Create matplotlib charts matching FOSSEE design system.
    
    Design rules (design.md Section 7):
    - No 3D, no gradients
    - Match colors exactly
    - White background
    - Grid alpha 0.1
    """
    records = list(dataset.records.all()[:15])  # Limit for readability
    
    if not records:
        return _create_empty_chart()
    
    equipment_names = [r.equipment_name[:12] for r in records]
    flowrates = [r.flowrate for r in records]
    pressures = [r.pressure for r in records]
    temperatures = [r.temperature for r in records]
    
    # Configure matplotlib to match design system
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.size': 10,
        'axes.facecolor': '#FFFFFF',
        'figure.facecolor': '#FFFFFF',
        'axes.edgecolor': '#E2E8F0',
        'axes.labelcolor': '#486581',
        'xtick.color': '#486581',
        'ytick.color': '#486581',
        'grid.alpha': 0.1,
        'grid.color': '#102A43',
    })
    
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.5))
    x = np.arange(len(equipment_names))
    
    # Flowrate chart
    axes[0].bar(x, flowrates, color=CHART_COLORS_HEX['flowrate'], width=0.7)
    axes[0].set_title('Flowrate', fontweight='600', color='#102A43', fontsize=12)
    axes[0].set_ylabel('Value', color='#486581', fontsize=10)
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(equipment_names, rotation=45, ha='right', fontsize=8)
    axes[0].grid(axis='y', alpha=0.1)
    
    # Pressure chart
    axes[1].bar(x, pressures, color=CHART_COLORS_HEX['pressure'], width=0.7)
    axes[1].set_title('Pressure', fontweight='600', color='#102A43', fontsize=12)
    axes[1].set_ylabel('Value', color='#486581', fontsize=10)
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(equipment_names, rotation=45, ha='right', fontsize=8)
    axes[1].grid(axis='y', alpha=0.1)
    
    # Temperature chart
    axes[2].bar(x, temperatures, color=CHART_COLORS_HEX['temperature'], width=0.7)
    axes[2].set_title('Temperature', fontweight='600', color='#102A43', fontsize=12)
    axes[2].set_ylabel('Value', color='#486581', fontsize=10)
    axes[2].set_xticks(x)
    axes[2].set_xticklabels(equipment_names, rotation=45, ha='right', fontsize=8)
    axes[2].grid(axis='y', alpha=0.1)
    
    plt.tight_layout()
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    buffer.seek(0)
    plt.close(fig)
    
    return buffer


def create_type_distribution_chart(dataset: Dataset) -> io.BytesIO:
    """Create pie chart for equipment type distribution"""
    records = dataset.records.all()
    
    if not records:
        return _create_empty_chart()
    
    # Calculate type distribution
    type_counts: dict[str, int] = {}
    for record in records:
        t = record.type
        type_counts[t] = type_counts.get(t, 0) + 1
    
    if not type_counts:
        return _create_empty_chart()
    
    labels = list(type_counts.keys())
    sizes = list(type_counts.values())
    chart_colors = CHART_COLORS_HEX['distribution'][:len(labels)]
    
    # Extend colors if needed
    while len(chart_colors) < len(labels):
        chart_colors.extend(CHART_COLORS_HEX['distribution'])
    
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.size': 10,
        'figure.facecolor': '#FFFFFF',
    })
    
    fig, ax = plt.subplots(figsize=(5, 4))
    
    wedges, texts, autotexts = ax.pie(
        sizes, 
        labels=labels,
        colors=chart_colors[:len(labels)],
        autopct='%1.1f%%',
        startangle=90,
        textprops={'fontsize': 10, 'color': '#102A43'}
    )
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    ax.set_title('Equipment Type Distribution', 
                 fontweight='600', color='#102A43', fontsize=12)
    
    plt.tight_layout()
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    buffer.seek(0)
    plt.close(fig)
    
    return buffer


def _create_empty_chart() -> io.BytesIO:
    """Create placeholder for empty data"""
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.text(0.5, 0.5, 'No data available', 
            ha='center', va='center', fontsize=14, color='#829AB1')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight',
                facecolor='white')
    buffer.seek(0)
    plt.close(fig)
    
    return buffer


# =============================================================================
# PDF Styles (design.md Section 12)
# =============================================================================

def get_pdf_styles() -> dict[str, ParagraphStyle]:
    """
    Create PDF styles following FOSSEE design system.
    
    - Serif headings (Times-Roman)
    - Mono tables (Courier)
    - FOSSEE colors
    """
    styles = getSampleStyleSheet()
    
    custom_styles = {
        # Main title - Serif, large
        'title': ParagraphStyle(
            'FOSSEETitle',
            parent=styles['Heading1'],
            fontName=FONTS['heading_bold'],
            fontSize=FONT_SIZES['h1'],
            textColor=COLORS['primary_900'],
            spaceAfter=8*mm,
            leading=36,
        ),
        
        # Section heading - Serif
        'heading': ParagraphStyle(
            'FOSSEEHeading',
            parent=styles['Heading2'],
            fontName=FONTS['heading_bold'],
            fontSize=FONT_SIZES['h2'],
            textColor=COLORS['primary_900'],
            spaceBefore=6*mm,
            spaceAfter=4*mm,
            leading=28,
        ),
        
        # Subsection heading - Serif
        'subheading': ParagraphStyle(
            'FOSSEESubheading',
            parent=styles['Heading3'],
            fontName=FONTS['heading'],
            fontSize=FONT_SIZES['h3'],
            textColor=COLORS['primary_700'],
            spaceBefore=4*mm,
            spaceAfter=2*mm,
            leading=24,
        ),
        
        # Body text - Sans-serif
        'body': ParagraphStyle(
            'FOSSEEBody',
            parent=styles['Normal'],
            fontName=FONTS['body'],
            fontSize=FONT_SIZES['body'],
            textColor=COLORS['text_primary'],
            leading=22,
        ),
        
        # Small text
        'small': ParagraphStyle(
            'FOSSEESmall',
            parent=styles['Normal'],
            fontName=FONTS['body'],
            fontSize=FONT_SIZES['small'],
            textColor=COLORS['text_secondary'],
            leading=18,
        ),
        
        # Mono text for data
        'mono': ParagraphStyle(
            'FOSSEEMono',
            parent=styles['Normal'],
            fontName=FONTS['mono'],
            fontSize=FONT_SIZES['mono'],
            textColor=COLORS['text_primary'],
            leading=18,
        ),
        
        # Footer/muted text
        'footer': ParagraphStyle(
            'FOSSEEFooter',
            parent=styles['Normal'],
            fontName=FONTS['body'],
            fontSize=FONT_SIZES['small'],
            textColor=COLORS['text_muted'],
            alignment=TA_CENTER,
            leading=16,
        ),
        
        # Card header
        'card_header': ParagraphStyle(
            'FOSSEECardHeader',
            parent=styles['Heading3'],
            fontName=FONTS['heading'],
            fontSize=FONT_SIZES['h3'],
            textColor=COLORS['primary_900'],
            spaceBefore=0,
            spaceAfter=2*mm,
        ),
        
        # Card value - large mono
        'card_value': ParagraphStyle(
            'FOSSEECardValue',
            parent=styles['Normal'],
            fontName=FONTS['mono_bold'],
            fontSize=24,
            textColor=COLORS['primary_700'],
            alignment=TA_CENTER,
            leading=30,
        ),
    }
    
    return custom_styles


def get_table_style() -> TableStyle:
    """
    Create table style following FOSSEE design.
    
    - Mono font for data
    - FOSSEE colors
    - Alternating rows
    """
    return TableStyle([
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), COLORS['primary_900']),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), FONTS['mono_bold']),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        
        # Body rows - Mono font
        ('FONTNAME', (0, 1), (-1, -1), FONTS['mono']),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TEXTCOLOR', (0, 1), (-1, -1), COLORS['text_primary']),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        
        # Grid
        ('GRID', (0, 0), (-1, -1), 0.5, COLORS['border']),
        
        # Alignment
        ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),  # Numeric columns right
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])


def get_alternating_row_style(num_rows: int) -> TableStyle:
    """Add alternating row colors to table"""
    style_commands = []
    for i in range(1, num_rows):
        if i % 2 == 0:
            style_commands.append(
                ('BACKGROUND', (0, i), (-1, i), COLORS['bg_main'])
            )
    return TableStyle(style_commands)


# =============================================================================
# Summary Cards
# =============================================================================

def create_summary_card(
    title: str, 
    value: str, 
    subtitle: str = ""
) -> Table:
    """
    Create a summary card matching Lab Panels design.
    
    Design (design.md Section 5.1):
    - Radius: 10
    - Top accent 3px primary-700
    - Shadow effect via borders
    """
    styles = get_pdf_styles()
    
    # Card content
    content = [
        [Paragraph(title, styles['card_header'])],
        [Paragraph(value, styles['card_value'])],
    ]
    
    if subtitle:
        content.append([Paragraph(subtitle, styles['small'])])
    
    # Create table as card
    card = Table(content, colWidths=[100])
    
    card.setStyle(TableStyle([
        # Card styling
        ('BACKGROUND', (0, 0), (-1, -1), COLORS['surface']),
        ('BOX', (0, 0), (-1, -1), 1, COLORS['border']),
        ('LINEABOVE', (0, 0), (-1, 0), 3, COLORS['primary_700']),  # Top accent
        
        # Padding
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 10),
        
        # Alignment
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    return card


def create_summary_cards_row(stats: dict[str, Any]) -> Table:
    """Create a row of summary cards for key metrics"""
    
    cards = [
        create_summary_card(
            "Total Records",
            str(stats.get('total_count', 0)),
            "equipment entries"
        ),
        create_summary_card(
            "Avg Flowrate",
            f"{stats.get('avg_flowrate', 0):.1f}",
            "units/sec"
        ),
        create_summary_card(
            "Avg Pressure",
            f"{stats.get('avg_pressure', 0):.1f}",
            "kPa"
        ),
        create_summary_card(
            "Avg Temperature",
            f"{stats.get('avg_temperature', 0):.1f}",
            "°C"
        ),
    ]
    
    # Arrange cards in a row
    row_table = Table([cards], colWidths=[120, 120, 120, 120])
    row_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    
    return row_table


# =============================================================================
# Main PDF Generator
# =============================================================================

def generate_pdf_report(dataset: Dataset) -> io.BytesIO:
    """
    Generate PDF report following FOSSEE design system.
    
    Content:
    - Header with branding
    - Summary cards
    - Statistical table
    - Charts as images
    - Data table preview
    """
    buffer = io.BytesIO()
    
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm
    )
    
    styles = get_pdf_styles()
    elements: list[Any] = []
    
    # =========================================================================
    # Header Section
    # =========================================================================
    elements.append(Paragraph('FOSSEE Scientific Analytics', styles['title']))
    elements.append(Paragraph('Chemical Equipment Parameter Report', styles['heading']))
    
    # Metadata line
    record_count = dataset.records.count()
    meta_text = (
        f"<b>Dataset:</b> {dataset.filename} &nbsp;&nbsp;|&nbsp;&nbsp; "
        f"<b>Records:</b> {record_count} &nbsp;&nbsp;|&nbsp;&nbsp; "
        f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )
    elements.append(Paragraph(meta_text, styles['small']))
    elements.append(Spacer(1, 8*mm))
    
    # =========================================================================
    # Summary Cards Section
    # =========================================================================
    elements.append(Paragraph('Summary Overview', styles['subheading']))
    
    # Calculate statistics
    from api.services import StatisticsService
    summary = StatisticsService.calculate_from_dataset(dataset.id) or {
        'total_count': record_count,
        'avg_flowrate': 0,
        'avg_pressure': 0,
        'avg_temperature': 0,
        'type_distribution': {}
    }
    
    # Add summary cards
    cards_row = create_summary_cards_row(summary)
    elements.append(cards_row)
    elements.append(Spacer(1, 8*mm))
    
    # =========================================================================
    # Statistical Summary Table
    # =========================================================================
    elements.append(Paragraph('Statistical Analysis', styles['subheading']))
    
    # Parse extended stats from summary_json
    ext_stats = None
    if dataset.summary_json:
        try:
            ext_stats = json.loads(dataset.summary_json) if isinstance(
                dataset.summary_json, str
            ) else dataset.summary_json
        except (json.JSONDecodeError, TypeError):
            ext_stats = None
    
    if ext_stats:
        stat_data = [
            ['Parameter', 'Min', 'Max', 'Mean', 'Std Dev'],
            [
                'Flowrate',
                f"{ext_stats.get('flowrate', {}).get('min', 0):.2f}",
                f"{ext_stats.get('flowrate', {}).get('max', 0):.2f}",
                f"{ext_stats.get('flowrate', {}).get('mean', 0):.2f}",
                f"{ext_stats.get('flowrate', {}).get('std', 0):.2f}",
            ],
            [
                'Pressure',
                f"{ext_stats.get('pressure', {}).get('min', 0):.2f}",
                f"{ext_stats.get('pressure', {}).get('max', 0):.2f}",
                f"{ext_stats.get('pressure', {}).get('mean', 0):.2f}",
                f"{ext_stats.get('pressure', {}).get('std', 0):.2f}",
            ],
            [
                'Temperature',
                f"{ext_stats.get('temperature', {}).get('min', 0):.2f}",
                f"{ext_stats.get('temperature', {}).get('max', 0):.2f}",
                f"{ext_stats.get('temperature', {}).get('mean', 0):.2f}",
                f"{ext_stats.get('temperature', {}).get('std', 0):.2f}",
            ],
        ]
        
        stat_table = Table(stat_data, colWidths=[100, 80, 80, 80, 80])
        stat_table.setStyle(get_table_style())
        stat_table.setStyle(get_alternating_row_style(len(stat_data)))
        elements.append(stat_table)
    
    elements.append(Spacer(1, 8*mm))
    
    # =========================================================================
    # Charts Section
    # =========================================================================
    elements.append(Paragraph('Parameter Visualizations', styles['subheading']))
    
    if record_count > 0:
        # Parameter bar charts
        chart_buffer = create_parameter_charts(dataset)
        chart_img = Image(chart_buffer, width=480, height=150)
        elements.append(chart_img)
        elements.append(Spacer(1, 6*mm))
        
        # Type distribution pie chart
        if summary.get('type_distribution'):
            elements.append(Paragraph('Type Distribution', styles['subheading']))
            pie_buffer = create_type_distribution_chart(dataset)
            pie_img = Image(pie_buffer, width=220, height=180)
            elements.append(pie_img)
    else:
        elements.append(Paragraph('No data available for charts', styles['body']))
    
    elements.append(Spacer(1, 8*mm))
    
    # =========================================================================
    # Data Table Preview
    # =========================================================================
    elements.append(Paragraph('Equipment Data Preview', styles['subheading']))
    
    records = dataset.records.all()[:20]  # Limit to 20 rows
    
    if records:
        table_data = [
            ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temp']
        ]
        
        for record in records:
            table_data.append([
                record.equipment_name[:25],
                record.type[:15],
                f"{record.flowrate:.2f}",
                f"{record.pressure:.2f}",
                f"{record.temperature:.2f}",
            ])
        
        data_table = Table(table_data, colWidths=[130, 90, 70, 70, 60])
        data_table.setStyle(get_table_style())
        data_table.setStyle(get_alternating_row_style(len(table_data)))
        elements.append(data_table)
        
        if record_count > 20:
            elements.append(Spacer(1, 2*mm))
            elements.append(Paragraph(
                f'Showing 20 of {record_count} records',
                styles['footer']
            ))
    else:
        elements.append(Paragraph('No records available', styles['body']))
    
    # =========================================================================
    # Footer
    # =========================================================================
    elements.append(Spacer(1, 12*mm))
    elements.append(HRFlowable(
        width="100%", 
        thickness=1, 
        color=COLORS['border'],
        spaceAfter=4*mm
    ))
    elements.append(Paragraph(
        'Generated by FOSSEE Scientific Analytics · IIT Bombay',
        styles['footer']
    ))
    elements.append(Paragraph(
        f'Report ID: {dataset.id} · {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        styles['footer']
    ))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    
    return buffer


# =============================================================================
# Utility exports for charts (used by other modules)
# =============================================================================

def create_chart(dataset: Dataset, chart_type: str = 'bar') -> io.BytesIO:
    """Legacy function - delegates to create_parameter_charts"""
    return create_parameter_charts(dataset)
