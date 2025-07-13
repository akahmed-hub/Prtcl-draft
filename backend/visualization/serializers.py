from rest_framework import serializers
from .models import Visualization, ChartData, ChartTemplate


class VisualizationSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    
    class Meta:
        model = Visualization
        fields = [
            'id', 'title', 'description', 'chart_type', 'chart_config',
            'data_source', 'created_by', 'created_at', 'updated_at',
            'is_public', 'shared_with'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']


class ChartDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartData
        fields = [
            'id', 'visualization', 'labels', 'datasets', 'metadata', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ChartTemplateSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    
    class Meta:
        model = ChartTemplate
        fields = [
            'id', 'name', 'description', 'chart_type', 'default_config',
            'is_public', 'created_by', 'created_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at'] 