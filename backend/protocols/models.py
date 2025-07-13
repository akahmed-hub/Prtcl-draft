from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class Protocol(models.Model):
    """Model for storing biological protocols."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='protocols')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)
    tags = models.JSONField(default=list, blank=True)
    
    # LLM generation metadata
    original_prompt = models.TextField(blank=True)
    llm_model_used = models.CharField(max_length=100, blank=True)
    generation_timestamp = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return self.title


class ProtocolStep(models.Model):
    """Model for individual steps within a protocol."""
    
    STEP_TYPES = [
        ('action', 'Action'),
        ('reagent', 'Reagent'),
        ('note', 'Note'),
        ('calculation', 'Calculation'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE, related_name='steps')
    step_number = models.PositiveIntegerField()
    step_type = models.CharField(max_length=20, choices=STEP_TYPES, default='action')
    title = models.CharField(max_length=200)
    content = models.TextField()
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    temperature_celsius = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # LLM-generated explanations
    reasoning = models.TextField(blank=True)
    alternatives = models.JSONField(default=list, blank=True)  # Store alternative parameters
    
    # User customization
    is_customized = models.BooleanField(default=False)
    custom_notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['step_number']
        unique_together = ['protocol', 'step_number']
    
    def __str__(self):
        return f"{self.protocol.title} - Step {self.step_number}: {self.title}"


class Reagent(models.Model):
    """Model for reagents used in protocols."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    concentration = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=50, blank=True)
    protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE, related_name='reagents')
    step = models.ForeignKey(ProtocolStep, on_delete=models.CASCADE, related_name='reagents', null=True, blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.concentration} {self.unit})"


class ResearchPaper(models.Model):
    """Model for storing research papers and their metadata."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=500)
    authors = models.JSONField(default=list)
    abstract = models.TextField(blank=True)
    doi = models.CharField(max_length=100, blank=True)
    pmid = models.CharField(max_length=20, blank=True)
    publication_date = models.DateField(null=True, blank=True)
    journal = models.CharField(max_length=200, blank=True)
    
    # File storage
    pdf_file = models.FileField(upload_to='papers/', null=True, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_papers')
    uploaded_at = models.DateTimeField(default=timezone.now)
    
    # Content extraction
    extracted_text = models.TextField(blank=True)
    keywords = models.JSONField(default=list, blank=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return self.title


class ProtocolReference(models.Model):
    """Model for linking protocols to research papers and other sources."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE, related_name='references')
    research_paper = models.ForeignKey(ResearchPaper, on_delete=models.CASCADE, related_name='protocol_references', null=True, blank=True)
    external_url = models.URLField(blank=True)
    reference_text = models.TextField()
    page_number = models.PositiveIntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['research_paper__title']
    
    def __str__(self):
        if self.research_paper:
            return f"{self.protocol.title} - {self.research_paper.title}"
        return f"{self.protocol.title} - {self.external_url}"


class ProtocolVersion(models.Model):
    """Model for tracking protocol versions."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    protocol = models.ForeignKey(Protocol, on_delete=models.CASCADE, related_name='versions')
    version_number = models.PositiveIntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    changes_summary = models.TextField(blank=True)
    
    # Store the complete protocol state at this version
    protocol_data = models.JSONField()  # Serialized protocol and steps data
    
    class Meta:
        ordering = ['-version_number']
        unique_together = ['protocol', 'version_number']
    
    def __str__(self):
        return f"{self.protocol.title} v{self.version_number}" 