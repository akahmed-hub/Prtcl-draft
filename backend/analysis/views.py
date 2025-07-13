from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import DataFile, AnalysisTask, AnalysisResult, qPCRData, WesternBlotData, AnalysisTemplate
from .serializers import (
    DataFileSerializer, AnalysisTaskSerializer, AnalysisResultSerializer,
    qPCRDataSerializer, WesternBlotDataSerializer, AnalysisTemplateSerializer
)


class DataFileViewSet(viewsets.ModelViewSet):
    """ViewSet for DataFile CRUD operations."""
    
    queryset = DataFile.objects.all()
    serializer_class = DataFileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['file_type', 'is_processed']
    search_fields = ['name', 'description']
    ordering_fields = ['uploaded_at', 'name']
    ordering = ['-uploaded_at']
    
    def get_queryset(self):
        """Filter files based on user permissions."""
        user = self.request.user
        if user.is_staff:
            return DataFile.objects.all()
        return DataFile.objects.filter(uploaded_by=user)
    
    def perform_create(self, serializer):
        """Set the uploader when creating a file."""
        serializer.save(uploaded_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        """Process the uploaded file."""
        data_file = self.get_object()
        
        # TODO: Implement file processing logic
        # This would involve:
        # 1. Parsing CSV files for qPCR data
        # 2. Processing TIFF files for Western Blot data
        # 3. Extracting relevant information
        
        return Response({'message': 'File processing started'})


class AnalysisTaskViewSet(viewsets.ModelViewSet):
    """ViewSet for AnalysisTask CRUD operations."""
    
    queryset = AnalysisTask.objects.all()
    serializer_class = AnalysisTaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['task_type', 'status']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'completed_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter tasks based on user permissions."""
        user = self.request.user
        if user.is_staff:
            return AnalysisTask.objects.all()
        return AnalysisTask.objects.filter(created_by=user)
    
    def perform_create(self, serializer):
        """Set the creator when creating a task."""
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """Start the analysis task."""
        task = self.get_object()
        
        # TODO: Implement task execution logic
        # This would involve:
        # 1. Updating task status to 'processing'
        # 2. Running the appropriate analysis
        # 3. Storing results
        
        return Response({'message': 'Analysis task started'})


class AnalysisResultViewSet(viewsets.ModelViewSet):
    """ViewSet for AnalysisResult CRUD operations."""
    
    queryset = AnalysisResult.objects.all()
    serializer_class = AnalysisResultSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter results based on user permissions."""
        user = self.request.user
        if user.is_staff:
            return AnalysisResult.objects.all()
        return AnalysisResult.objects.filter(task__created_by=user)


class qPCRDataViewSet(viewsets.ModelViewSet):
    """ViewSet for qPCRData CRUD operations."""
    
    queryset = qPCRData.objects.all()
    serializer_class = qPCRDataSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter data based on user permissions."""
        user = self.request.user
        if user.is_staff:
            return qPCRData.objects.all()
        return qPCRData.objects.filter(data_file__uploaded_by=user)


class WesternBlotDataViewSet(viewsets.ModelViewSet):
    """ViewSet for WesternBlotData CRUD operations."""
    
    queryset = WesternBlotData.objects.all()
    serializer_class = WesternBlotDataSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter data based on user permissions."""
        user = self.request.user
        if user.is_staff:
            return WesternBlotData.objects.all()
        return WesternBlotData.objects.filter(data_file__uploaded_by=user)


class AnalysisTemplateViewSet(viewsets.ModelViewSet):
    """ViewSet for AnalysisTemplate CRUD operations."""
    
    queryset = AnalysisTemplate.objects.all()
    serializer_class = AnalysisTemplateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['task_type', 'is_public']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter templates based on user permissions."""
        user = self.request.user
        if user.is_staff:
            return AnalysisTemplate.objects.all()
        from django.db import models
        return AnalysisTemplate.objects.filter(
            models.Q(created_by=user) | models.Q(is_public=True)
        )
    
    def perform_create(self, serializer):
        """Set the creator when creating a template."""
        serializer.save(created_by=self.request.user) 