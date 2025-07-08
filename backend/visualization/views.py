from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Visualization, ChartData, ChartTemplate
from .serializers import (
    VisualizationSerializer, ChartDataSerializer, ChartTemplateSerializer
)


class VisualizationViewSet(viewsets.ModelViewSet):
    """ViewSet for Visualization CRUD operations."""
    
    queryset = Visualization.objects.all()
    serializer_class = VisualizationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['chart_type', 'is_public']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-updated_at']
    
    def get_queryset(self):
        """Filter visualizations based on user permissions."""
        user = self.request.user
        if user.is_staff:
            return Visualization.objects.all()
        from django.db import models
        from django.contrib.auth.models import User
        return Visualization.objects.filter(
            models.Q(created_by=user) | 
            models.Q(is_public=True) | 
            models.Q(shared_with=user)
        ).distinct()
    
    def perform_create(self, serializer):
        """Set the creator when creating a visualization."""
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def share(self, request, pk=None):
        """Share visualization with other users."""
        visualization = self.get_object()
        user_ids = request.data.get('user_ids', [])
        
        # Add users to shared_with
        users = User.objects.filter(id__in=user_ids)
        visualization.shared_with.add(*users)
        
        return Response({'message': 'Visualization shared successfully'})
    
    @action(detail=True, methods=['post'])
    def export(self, request, pk=None):
        """Export visualization data."""
        visualization = self.get_object()
        
        # TODO: Implement export functionality
        # This could export to PNG, PDF, or other formats
        
        return Response({'message': 'Export functionality coming soon'})


class ChartDataViewSet(viewsets.ModelViewSet):
    """ViewSet for ChartData CRUD operations."""
    
    queryset = ChartData.objects.all()
    serializer_class = ChartDataSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter chart data based on user permissions."""
        user = self.request.user
        if user.is_staff:
            return ChartData.objects.all()
        return ChartData.objects.filter(
            visualization__created_by=user
        )


class ChartTemplateViewSet(viewsets.ModelViewSet):
    """ViewSet for ChartTemplate CRUD operations."""
    
    queryset = ChartTemplate.objects.all()
    serializer_class = ChartTemplateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['chart_type', 'is_public']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter templates based on user permissions."""
        user = self.request.user
        if user.is_staff:
            return ChartTemplate.objects.all()
        return ChartTemplate.objects.filter(
            models.Q(created_by=user) | models.Q(is_public=True)
        )
    
    def perform_create(self, serializer):
        """Set the creator when creating a template."""
        serializer.save(created_by=self.request.user) 