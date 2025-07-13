from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class DataFile(models.Model):
    """Model for storing uploaded data files."""
    
    FILE_TYPES = [
        ('qpc_csv', 'qPCR CSV'),
        ('western_tiff', 'Western Blot TIFF'),
        ('excel', 'Excel File'),
        ('csv', 'CSV File'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    file_type = models.CharField(max_length=20, choices=FILE_TYPES)
    file = models.FileField(upload_to='data_files/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='data_files')
    uploaded_at = models.DateTimeField(default=timezone.now)
    
    # File metadata
    file_size = models.BigIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    tags = models.JSONField(default=list, blank=True)
    
    # Processing status
    is_processed = models.BooleanField(default=False)
    processing_error = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.name} ({self.get_file_type_display()})"


class AnalysisTask(models.Model):
    """Model for tracking analysis tasks."""
    
    TASK_TYPES = [
        ('qpcr_delta_ct', 'qPCR Delta Ct'),
        ('qpcr_delta_delta_ct', 'qPCR Delta-Delta Ct'),
        ('western_quantification', 'Western Blot Quantification'),
        ('western_normalization', 'Western Blot Normalization'),
        ('custom', 'Custom Analysis'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task_type = models.CharField(max_length=30, choices=TASK_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Task details
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    parameters = models.JSONField(default=dict)  # Analysis parameters
    
    # Associated data
    data_files = models.ManyToManyField(DataFile, related_name='analysis_tasks')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='analysis_tasks')
    
    # Timing
    created_at = models.DateTimeField(default=timezone.now)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Results
    result_file = models.FileField(upload_to='analysis_results/', null=True, blank=True)
    result_data = models.JSONField(default=dict)  # Structured results
    error_message = models.TextField(blank=True)
    
    # Celery task tracking
    celery_task_id = models.CharField(max_length=255, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.get_task_type_display()})"


class AnalysisResult(models.Model):
    """Model for storing detailed analysis results."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey(AnalysisTask, on_delete=models.CASCADE, related_name='results')
    
    # Result data
    result_type = models.CharField(max_length=50)  # e.g., 'delta_ct_values', 'band_intensities'
    data = models.JSONField()  # Structured result data
    metadata = models.JSONField(default=dict)  # Additional metadata
    
    # Visualization data
    chart_data = models.JSONField(default=dict)  # Data formatted for charts
    chart_config = models.JSONField(default=dict)  # Chart configuration
    
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.task.name} - {self.result_type}"


class qPCRData(models.Model):
    """Model for storing qPCR-specific data."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data_file = models.ForeignKey(DataFile, on_delete=models.CASCADE, related_name='qpcr_data')
    
    # Sample information
    sample_name = models.CharField(max_length=100)
    target_gene = models.CharField(max_length=100)
    ct_value = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    ct_mean = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    ct_std = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    
    # Analysis results
    delta_ct = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    delta_delta_ct = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    fold_change = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    
    # Metadata
    replicate_number = models.PositiveIntegerField(default=1)
    is_control = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['sample_name', 'target_gene', 'replicate_number']
    
    def __str__(self):
        return f"{self.sample_name} - {self.target_gene}"


class WesternBlotData(models.Model):
    """Model for storing Western Blot-specific data."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data_file = models.ForeignKey(DataFile, on_delete=models.CASCADE, related_name='western_data')
    
    # Band information
    band_name = models.CharField(max_length=100)
    lane_number = models.PositiveIntegerField()
    molecular_weight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    
    # Intensity measurements
    raw_intensity = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    background_subtracted = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    normalized_intensity = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    
    # Analysis results
    relative_expression = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    fold_change = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    
    # Metadata
    is_loading_control = models.BooleanField(default=False)
    is_target_protein = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['lane_number', 'molecular_weight']
    
    def __str__(self):
        return f"Lane {self.lane_number} - {self.band_name}"


class AnalysisTemplate(models.Model):
    """Model for storing reusable analysis templates."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Template configuration
    task_type = models.CharField(max_length=30, choices=AnalysisTask.TASK_TYPES)
    parameters = models.JSONField(default=dict)
    is_public = models.BooleanField(default=False)
    
    # Ownership
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='analysis_templates')
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name 