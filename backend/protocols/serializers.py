from rest_framework import serializers
from .models import Protocol, ProtocolStep, Reagent, ResearchPaper, ProtocolReference, ProtocolVersion


class ReagentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reagent
        fields = ['id', 'name', 'concentration', 'unit']


class ProtocolStepSerializer(serializers.ModelSerializer):
    reagents = ReagentSerializer(many=True, read_only=True)
    
    class Meta:
        model = ProtocolStep
        fields = [
            'id', 'step_number', 'step_type', 'title', 'content',
            'duration_minutes', 'temperature_celsius', 'reasoning',
            'alternatives', 'is_customized', 'custom_notes', 'reagents'
        ]


class ProtocolStepCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtocolStep
        fields = [
            'step_number', 'step_type', 'title', 'content',
            'duration_minutes', 'temperature_celsius'
        ]


class ProtocolSerializer(serializers.ModelSerializer):
    steps = ProtocolStepSerializer(many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.username')
    
    class Meta:
        model = Protocol
        fields = [
            'id', 'title', 'description', 'author', 'created_at',
            'updated_at', 'is_public', 'tags', 'original_prompt',
            'llm_model_used', 'generation_timestamp', 'steps'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'author']


class ProtocolCreateSerializer(serializers.ModelSerializer):
    steps = ProtocolStepCreateSerializer(many=True, required=False)
    
    class Meta:
        model = Protocol
        fields = [
            'title', 'description', 'is_public', 'tags',
            'original_prompt', 'steps'
        ]
    
    def create(self, validated_data):
        steps_data = validated_data.pop('steps', [])
        protocol = Protocol.objects.create(**validated_data)
        
        for step_data in steps_data:
            ProtocolStep.objects.create(protocol=protocol, **step_data)
        
        return protocol


class ProtocolUpdateSerializer(serializers.ModelSerializer):
    steps = ProtocolStepSerializer(many=True, required=False)
    
    class Meta:
        model = Protocol
        fields = [
            'title', 'description', 'is_public', 'tags', 'steps'
        ]
    
    def update(self, instance, validated_data):
        steps_data = validated_data.pop('steps', [])
        
        # Update protocol fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update steps if provided
        if steps_data:
            # Clear existing steps
            instance.steps.all().delete()
            
            # Create new steps
            for step_data in steps_data:
                ProtocolStep.objects.create(protocol=instance, **step_data)
        
        return instance


class ResearchPaperSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.ReadOnlyField(source='uploaded_by.username')
    
    class Meta:
        model = ResearchPaper
        fields = [
            'id', 'title', 'authors', 'abstract', 'doi', 'pmid',
            'publication_date', 'journal', 'pdf_file', 'uploaded_by',
            'uploaded_at', 'keywords'
        ]
        read_only_fields = ['id', 'uploaded_by', 'uploaded_at']


class ProtocolReferenceSerializer(serializers.ModelSerializer):
    research_paper = ResearchPaperSerializer(read_only=True)
    
    class Meta:
        model = ProtocolReference
        fields = [
            'id', 'research_paper', 'external_url', 'reference_text',
            'page_number'
        ]


class ProtocolVersionSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    
    class Meta:
        model = ProtocolVersion
        fields = [
            'id', 'version_number', 'created_at', 'created_by',
            'changes_summary', 'protocol_data'
        ]
        read_only_fields = ['id', 'created_at', 'created_by']


class ProtocolGenerationRequestSerializer(serializers.Serializer):
    """Serializer for protocol generation requests."""
    prompt = serializers.CharField(max_length=2000)
    include_reagents = serializers.BooleanField(default=True)
    include_reasoning = serializers.BooleanField(default=True)
    cross_reference_papers = serializers.BooleanField(default=True)
    max_steps = serializers.IntegerField(min_value=1, max_value=50, default=20)
    
    def validate_prompt(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Prompt must be at least 10 characters long.")
        return value


class ProtocolSearchSerializer(serializers.Serializer):
    """Serializer for protocol search requests."""
    query = serializers.CharField(max_length=500)
    search_type = serializers.ChoiceField(
        choices=['keyword', 'semantic', 'both'],
        default='keyword'
    )
    filters = serializers.JSONField(required=False, default=dict)
    limit = serializers.IntegerField(min_value=1, max_value=100, default=20) 