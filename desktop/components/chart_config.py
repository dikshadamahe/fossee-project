"""
Matplotlib Configuration for FOSSEE Scientific Analytics UI
Ensures visual consistency with the web Chart.js implementation
"""

import matplotlib.pyplot as plt
import matplotlib as mpl

# Design tokens from FOSSEE Scientific Analytics UI
COLORS = {
    'primary_900': '#0F2A44',
    'primary_700': '#1B7F79',
    'primary_600': '#3A4E9F',
    'success': '#2EA043',
    'warning': '#D97706',
    'error': '#C53030',
    'bg_main': '#F7F9FC',
    'surface': '#FFFFFF',
    'border': '#E2E8F0',
    'text_primary': '#102A43',
    'text_secondary': '#486581',
    'text_muted': '#829AB1',
}

CHART_COLORS = {
    'flowrate': '#1B7F79',
    'pressure': '#3A4E9F',
    'temperature': '#C53030',
    'distribution': ['#1B7F79', '#3A4E9F', '#2EA043', '#D97706'],
}


def configure_matplotlib():
    """Configure matplotlib to match design system"""
    
    # Use a clean style as base
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # Custom configuration
    mpl.rcParams.update({
        # Figure
        'figure.facecolor': COLORS['surface'],
        'figure.edgecolor': COLORS['surface'],
        'figure.dpi': 100,
        
        # Axes
        'axes.facecolor': COLORS['surface'],
        'axes.edgecolor': COLORS['border'],
        'axes.labelcolor': COLORS['text_secondary'],
        'axes.titlecolor': COLORS['text_primary'],
        'axes.titleweight': '600',
        'axes.titlesize': 14,
        'axes.labelsize': 11,
        'axes.linewidth': 0.5,
        'axes.grid': True,
        'axes.spines.top': False,
        'axes.spines.right': False,
        
        # Grid
        'grid.color': COLORS['border'],
        'grid.alpha': 0.3,
        'grid.linewidth': 0.5,
        
        # Ticks
        'xtick.color': COLORS['text_muted'],
        'ytick.color': COLORS['text_secondary'],
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        
        # Legend
        'legend.frameon': True,
        'legend.facecolor': COLORS['surface'],
        'legend.edgecolor': COLORS['border'],
        'legend.fontsize': 11,
        'legend.loc': 'lower center',
        
        # Font
        'font.family': 'sans-serif',
        'font.sans-serif': ['Segoe UI', 'Noto Sans', 'DejaVu Sans'],
        'font.size': 11,
        
        # Lines
        'lines.linewidth': 2,
        'lines.markersize': 6,
        
        # Patches (bars, etc)
        'patch.linewidth': 0,
    })


def create_bar_chart(ax, labels, data, color_key='flowrate', title=None):
    """Create a bar chart following design system"""
    
    color = CHART_COLORS.get(color_key, CHART_COLORS['flowrate'])
    
    bars = ax.bar(labels, data, color=color, width=0.7, edgecolor='none')
    
    if title:
        ax.set_title(title, fontweight='600', color=COLORS['text_primary'])
    
    # Style adjustments
    ax.tick_params(axis='x', rotation=45)
    ax.set_axisbelow(True)
    
    return bars


def create_multi_bar_chart(ax, labels, datasets, title=None):
    """Create a grouped bar chart for multiple parameters"""
    
    import numpy as np
    
    x = np.arange(len(labels))
    width = 0.25
    
    bars = []
    for i, (key, data) in enumerate(datasets.items()):
        color = CHART_COLORS.get(key, CHART_COLORS['distribution'][i])
        offset = (i - len(datasets) / 2 + 0.5) * width
        bar = ax.bar(x + offset, data, width, label=key.capitalize(), color=color)
        bars.append(bar)
    
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.legend(loc='upper right')
    
    if title:
        ax.set_title(title, fontweight='600', color=COLORS['text_primary'])
    
    return bars


def create_pie_chart(ax, labels, data, title=None):
    """Create a pie/doughnut chart following design system"""
    
    colors = CHART_COLORS['distribution'][:len(data)]
    
    wedges, texts, autotexts = ax.pie(
        data,
        labels=labels,
        colors=colors,
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops={'edgecolor': COLORS['surface'], 'linewidth': 2},
        textprops={'fontsize': 10, 'color': COLORS['text_primary']},
    )
    
    # Style percentage text
    for autotext in autotexts:
        autotext.set_fontsize(9)
        autotext.set_fontfamily('monospace')
    
    ax.axis('equal')
    
    if title:
        ax.set_title(title, fontweight='600', color=COLORS['text_primary'], pad=20)
    
    return wedges
