from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class Visualization(models.Model):
    """Model for storing data visualizations."""
    
    CHART_TYPES = [
        ('bar', 'Bar Chart'),
        ('line', 'Line Chart'),
        ('scatter', 'Scatter Plot'),
        ('pie', 'Pie Chart'),
        ('heatmap', 'Heatmap'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    chart_type = models.CharField(max_length=20, choices=CHART_TYPES)
    
    # Chart configuration
    chart_config = models.JSONField(default=dict)  # Chart.js configuration
    data_source = models.JSONField(default=dict)  # Data source information
    
    # Ownership
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visualizations')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Sharing
    is_public = models.BooleanField(default=False)
    shared_with = models.ManyToManyField(User, related_name='shared_visualizations', blank=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return self.title


class ChartData(models.Model):
    """Model for storing chart data."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    visualization = models.ForeignKey(Visualization, on_delete=models.CASCADE, related_name='chart_data')
    
    # Data structure
    labels = models.JSONField(default=list)  # X-axis labels
    datasets = models.JSONField(default=list)  # Y-axis data series
    metadata = models.JSONField(default=dict)  # Additional metadata
    
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.visualization.title} - Data"


class ChartTemplate(models.Model):
    """Model for storing reusable chart templates."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Template configuration
    chart_type = models.CharField(max_length=20, choices=Visualization.CHART_TYPES)
    default_config = models.JSONField(default=dict)
    is_public = models.BooleanField(default=False)
    
    # Ownership
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chart_templates')
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name 