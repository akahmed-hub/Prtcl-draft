from rest_framework import serializers
from .models import DataFile, AnalysisTask, AnalysisResult, qPCRData, WesternBlotData, AnalysisTemplate


class DataFileSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.ReadOnlyField(source='uploaded_by.username')
    
    class Meta:
        model = DataFile
        fields = [
            'id', 'name', 'file_type', 'file', 'uploaded_by', 'uploaded_at',
            'file_size', 'description', 'tags', 'is_processed', 'processing_error'
        ]
        read_only_fields = ['id', 'uploaded_by', 'uploaded_at', 'file_size']


class AnalysisTaskSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    data_files = DataFileSerializer(many=True, read_only=True)
    
    class Meta:
        model = AnalysisTask
        fields = [
            'id', 'task_type', 'status', 'name', 'description', 'parameters',
            'data_files', 'created_by', 'created_at', 'started_at', 'completed_at',
            'result_file', 'result_data', 'error_message', 'celery_task_id'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'started_at', 'completed_at']


class AnalysisResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisResult
        fields = [
            'id', 'task', 'result_type', 'data', 'metadata',
            'chart_data', 'chart_config', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class qPCRDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = qPCRData
        fields = [
            'id', 'data_file', 'sample_name', 'target_gene', 'ct_value',
            'ct_mean', 'ct_std', 'delta_ct', 'delta_delta_ct', 'fold_change',
            'replicate_number', 'is_control', 'notes'
        ]
        read_only_fields = ['id']


class WesternBlotDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WesternBlotData
        fields = [
            'id', 'data_file', 'band_name', 'lane_number', 'molecular_weight',
            'raw_intensity', 'background_subtracted', 'normalized_intensity',
            'relative_expression', 'fold_change', 'is_loading_control',
            'is_target_protein', 'notes'
        ]
        read_only_fields = ['id']


class AnalysisTemplateSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    
    class Meta:
        model = AnalysisTemplate
        fields = [
            'id', 'name', 'description', 'task_type', 'parameters',
            'is_public', 'created_by', 'created_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at'] 