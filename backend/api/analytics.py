"""
Analytics Service for Chemical Equipment Parameter Visualizer
Pandas-based statistical analysis with Python 3.12 type hints
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypedDict, Any
from enum import Enum

import pandas as pd
import numpy as np


class HealthStatus(Enum):
    """Equipment health status categories"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    CRITICAL = "critical"


class ParameterStats(TypedDict):
    """Statistics for a single numeric parameter"""
    min: float
    max: float
    mean: float
    median: float
    std: float
    q1: float
    q3: float
    iqr: float


class OutlierInfo(TypedDict):
    """Information about detected outliers"""
    equipment_name: str
    parameter: str
    value: float
    lower_bound: float
    upper_bound: float
    deviation_type: str  # 'low' or 'high'


class TypeDistribution(TypedDict):
    """Equipment type distribution"""
    type: str
    count: int
    percentage: float


class HealthScoreResult(TypedDict):
    """Health score calculation result"""
    equipment_name: str
    health_score: int
    status: str
    factors: dict[str, float]


class AnalyticsResult(TypedDict):
    """Complete analytics result"""
    parameter_stats: dict[str, ParameterStats]
    type_distribution: list[TypeDistribution]
    outliers: list[OutlierInfo]
    health_scores: list[HealthScoreResult]
    summary: dict[str, Any]


@dataclass
class AnalyticsConfig:
    """Configuration for analytics calculations"""
    iqr_multiplier: float = 1.5
    health_weights: dict[str, float] = field(default_factory=lambda: {
        'flowrate': 0.35,
        'pressure': 0.35,
        'temperature': 0.30
    })
    # Optimal ranges for health scoring (equipment-specific defaults)
    optimal_ranges: dict[str, tuple[float, float]] = field(default_factory=lambda: {
        'flowrate': (50.0, 200.0),
        'pressure': (30.0, 80.0),
        'temperature': (20.0, 40.0)
    })


class AnalyticsService:
    """
    Pandas-based analytics service for equipment data analysis.
    
    Provides:
    - Statistical analysis (mean, min, max, std, quartiles)
    - Equipment type distribution
    - Outlier detection using IQR method
    - Health score calculation (0-100)
    """
    
    NUMERIC_COLUMNS: list[str] = ['Flowrate', 'Pressure', 'Temperature']
    
    def __init__(self, config: AnalyticsConfig | None = None) -> None:
        """Initialize analytics service with optional configuration"""
        self.config = config or AnalyticsConfig()
    
    @staticmethod
    def calculate_parameter_stats(df: pd.DataFrame) -> dict[str, ParameterStats]:
        """
        Calculate comprehensive statistics for numeric columns.
        
        Args:
            df: DataFrame with Flowrate, Pressure, Temperature columns
            
        Returns:
            Dictionary mapping parameter names to their statistics
        """
        stats: dict[str, ParameterStats] = {}
        
        for column in AnalyticsService.NUMERIC_COLUMNS:
            if column not in df.columns:
                continue
                
            series = pd.to_numeric(df[column], errors='coerce').dropna()
            
            if series.empty:
                stats[column.lower()] = ParameterStats(
                    min=0.0, max=0.0, mean=0.0, median=0.0,
                    std=0.0, q1=0.0, q3=0.0, iqr=0.0
                )
                continue
            
            q1 = float(series.quantile(0.25))
            q3 = float(series.quantile(0.75))
            
            stats[column.lower()] = ParameterStats(
                min=float(series.min()),
                max=float(series.max()),
                mean=float(series.mean()),
                median=float(series.median()),
                std=float(series.std()) if len(series) > 1 else 0.0,
                q1=q1,
                q3=q3,
                iqr=q3 - q1
            )
        
        return stats
    
    @staticmethod
    def calculate_type_distribution(df: pd.DataFrame) -> list[TypeDistribution]:
        """
        Calculate equipment type distribution with counts and percentages.
        
        Args:
            df: DataFrame with 'Type' column
            
        Returns:
            List of type distributions sorted by count descending
        """
        if 'Type' not in df.columns:
            return []
        
        total = len(df)
        if total == 0:
            return []
        
        type_counts = df['Type'].value_counts()
        
        distributions: list[TypeDistribution] = []
        for equipment_type, count in type_counts.items():
            distributions.append(TypeDistribution(
                type=str(equipment_type),
                count=int(count),
                percentage=round((count / total) * 100, 2)
            ))
        
        return distributions
    
    def detect_outliers(
        self, 
        df: pd.DataFrame,
        iqr_multiplier: float | None = None
    ) -> list[OutlierInfo]:
        """
        Detect outliers using IQR (Interquartile Range) method.
        
        Outliers are values that fall below Q1 - (multiplier * IQR) or
        above Q3 + (multiplier * IQR).
        
        Args:
            df: DataFrame with equipment data
            iqr_multiplier: IQR multiplier (default 1.5 for standard outliers)
            
        Returns:
            List of detected outliers with details
        """
        multiplier = iqr_multiplier or self.config.iqr_multiplier
        outliers: list[OutlierInfo] = []
        
        # Need equipment name column
        name_col = 'Equipment Name' if 'Equipment Name' in df.columns else 'equipment_name'
        if name_col not in df.columns:
            return outliers
        
        for column in self.NUMERIC_COLUMNS:
            if column not in df.columns:
                continue
            
            series = pd.to_numeric(df[column], errors='coerce')
            
            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)
            iqr = q3 - q1
            
            lower_bound = q1 - (multiplier * iqr)
            upper_bound = q3 + (multiplier * iqr)
            
            # Find outliers
            low_outliers = df[series < lower_bound]
            high_outliers = df[series > upper_bound]
            
            for _, row in low_outliers.iterrows():
                outliers.append(OutlierInfo(
                    equipment_name=str(row[name_col]),
                    parameter=column.lower(),
                    value=float(row[column]),
                    lower_bound=float(lower_bound),
                    upper_bound=float(upper_bound),
                    deviation_type='low'
                ))
            
            for _, row in high_outliers.iterrows():
                outliers.append(OutlierInfo(
                    equipment_name=str(row[name_col]),
                    parameter=column.lower(),
                    value=float(row[column]),
                    lower_bound=float(lower_bound),
                    upper_bound=float(upper_bound),
                    deviation_type='high'
                ))
        
        return outliers
    
    def calculate_health_score(
        self, 
        df: pd.DataFrame,
        optimal_ranges: dict[str, tuple[float, float]] | None = None
    ) -> list[HealthScoreResult]:
        """
        Calculate health score (0-100) for each equipment based on parameters.
        
        Health score is calculated by:
        1. Measuring how close each parameter is to its optimal range
        2. Applying configurable weights to each parameter
        3. Combining into a weighted score
        
        Args:
            df: DataFrame with equipment data
            optimal_ranges: Optional custom optimal ranges per parameter
            
        Returns:
            List of health scores with breakdown factors
        """
        ranges = optimal_ranges or self.config.optimal_ranges
        weights = self.config.health_weights
        
        results: list[HealthScoreResult] = []
        
        # Determine name column
        name_col = 'Equipment Name' if 'Equipment Name' in df.columns else 'equipment_name'
        if name_col not in df.columns:
            return results
        
        for _, row in df.iterrows():
            factors: dict[str, float] = {}
            weighted_sum = 0.0
            total_weight = 0.0
            
            for column in self.NUMERIC_COLUMNS:
                param_key = column.lower()
                
                if column not in df.columns or param_key not in ranges:
                    continue
                
                try:
                    value = float(row[column])
                except (ValueError, TypeError):
                    continue
                
                optimal_min, optimal_max = ranges[param_key]
                weight = weights.get(param_key, 0.33)
                
                # Calculate parameter score (0-100)
                param_score = self._calculate_parameter_score(
                    value, optimal_min, optimal_max
                )
                
                factors[param_key] = round(param_score, 2)
                weighted_sum += param_score * weight
                total_weight += weight
            
            # Calculate final health score
            if total_weight > 0:
                health_score = int(round(weighted_sum / total_weight))
            else:
                health_score = 0
            
            # Clamp to 0-100
            health_score = max(0, min(100, health_score))
            
            results.append(HealthScoreResult(
                equipment_name=str(row[name_col]),
                health_score=health_score,
                status=self._get_health_status(health_score).value,
                factors=factors
            ))
        
        return results
    
    @staticmethod
    def _calculate_parameter_score(
        value: float, 
        optimal_min: float, 
        optimal_max: float
    ) -> float:
        """
        Calculate score for a parameter value based on optimal range.
        
        Returns 100 if within range, decreasing score as value deviates.
        """
        if optimal_min <= value <= optimal_max:
            return 100.0
        
        # Calculate how far outside the range
        range_size = optimal_max - optimal_min
        if range_size == 0:
            range_size = 1.0
        
        if value < optimal_min:
            deviation = optimal_min - value
        else:
            deviation = value - optimal_max
        
        # Score decreases exponentially with deviation
        # At 1x range deviation = ~37% score, at 2x = ~13%
        deviation_ratio = deviation / range_size
        score = 100.0 * np.exp(-deviation_ratio)
        
        return max(0.0, score)
    
    @staticmethod
    def _get_health_status(score: int) -> HealthStatus:
        """Map health score to status category"""
        if score >= 90:
            return HealthStatus.EXCELLENT
        elif score >= 75:
            return HealthStatus.GOOD
        elif score >= 50:
            return HealthStatus.FAIR
        elif score >= 25:
            return HealthStatus.POOR
        else:
            return HealthStatus.CRITICAL
    
    def analyze(self, df: pd.DataFrame) -> AnalyticsResult:
        """
        Perform complete analytics on equipment data.
        
        Args:
            df: DataFrame with equipment data
            
        Returns:
            Complete analytics result with all metrics
        """
        # Normalize column names if needed
        df = self._normalize_columns(df)
        
        # Calculate all analytics
        parameter_stats = self.calculate_parameter_stats(df)
        type_distribution = self.calculate_type_distribution(df)
        outliers = self.detect_outliers(df)
        health_scores = self.calculate_health_score(df)
        
        # Calculate summary statistics
        avg_health = (
            sum(h['health_score'] for h in health_scores) / len(health_scores)
            if health_scores else 0.0
        )
        
        status_counts: dict[str, int] = {}
        for h in health_scores:
            status = h['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        summary: dict[str, Any] = {
            'total_records': len(df),
            'total_outliers': len(outliers),
            'average_health_score': round(avg_health, 1),
            'health_status_distribution': status_counts,
            'equipment_types_count': len(type_distribution),
        }
        
        return AnalyticsResult(
            parameter_stats=parameter_stats,
            type_distribution=type_distribution,
            outliers=outliers,
            health_scores=health_scores,
            summary=summary
        )
    
    @staticmethod
    def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Normalize column names to expected format"""
        column_mapping = {
            'equipment_name': 'Equipment Name',
            'type': 'Type',
            'flowrate': 'Flowrate',
            'flow_rate': 'Flowrate',
            'pressure': 'Pressure',
            'temperature': 'Temperature',
            'temp': 'Temperature',
        }
        
        df = df.copy()
        rename_map = {}
        
        for col in df.columns:
            col_lower = col.lower().strip()
            if col_lower in column_mapping:
                rename_map[col] = column_mapping[col_lower]
        
        if rename_map:
            df.rename(columns=rename_map, inplace=True)
        
        return df
    
    @classmethod
    def from_records(
        cls, 
        records: list[dict[str, Any]],
        config: AnalyticsConfig | None = None
    ) -> AnalyticsResult:
        """
        Create analytics from a list of record dictionaries.
        
        Args:
            records: List of equipment record dictionaries
            config: Optional analytics configuration
            
        Returns:
            Complete analytics result
        """
        df = pd.DataFrame(records)
        service = cls(config)
        return service.analyze(df)
