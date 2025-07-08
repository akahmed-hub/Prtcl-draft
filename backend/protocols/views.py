from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Protocol, ProtocolStep, Reagent, ResearchPaper, ProtocolReference
from .serializers import (
    ProtocolSerializer, ProtocolCreateSerializer, ProtocolUpdateSerializer,
    ProtocolStepSerializer, ReagentSerializer, ResearchPaperSerializer,
    ProtocolReferenceSerializer, ProtocolGenerationRequestSerializer,
    ProtocolSearchSerializer
)
from .services import ProtocolService


class ProtocolViewSet(viewsets.ModelViewSet):
    """ViewSet for Protocol CRUD operations."""
    
    queryset = Protocol.objects.all()
    serializer_class = ProtocolSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_public', 'author', 'tags']
    search_fields = ['title', 'description', 'original_prompt']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-updated_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ProtocolCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ProtocolUpdateSerializer
        return ProtocolSerializer
    
    def get_queryset(self):
        """Filter protocols based on user permissions."""
        user = self.request.user
        if user.is_staff:
            return Protocol.objects.all()
        return Protocol.objects.filter(
            models.Q(author=user) | models.Q(is_public=True)
        )
    
    def perform_create(self, serializer):
        """Set the author when creating a protocol."""
        serializer.save(author=self.request.user)
    
    @swagger_auto_schema(
        request_body=ProtocolGenerationRequestSerializer,
        responses={201: ProtocolSerializer}
    )
    @action(detail=False, methods=['post'])
    def generate(self, request):
        """Generate a protocol using LLM."""
        serializer = ProtocolGenerationRequestSerializer(data=request.data)
        if serializer.is_valid():
            try:
                service = ProtocolService()
                protocol = service.create_protocol_from_prompt(
                    user=request.user,
                    **serializer.validated_data
                )
                
                response_serializer = ProtocolSerializer(protocol)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                return Response(
                    {'error': f'Failed to generate protocol: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        request_body=ProtocolSearchSerializer,
        responses={200: ProtocolSerializer(many=True)}
    )
    @action(detail=False, methods=['post'])
    def search(self, request):
        """Search for protocols."""
        serializer = ProtocolSearchSerializer(data=request.data)
        if serializer.is_valid():
            service = ProtocolService()
            protocols = service.search_protocols(**serializer.validated_data)
            
            response_serializer = ProtocolSerializer(protocols, many=True)
            return Response(response_serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """Duplicate an existing protocol."""
        protocol = self.get_object()
        
        # Create a copy
        new_protocol = Protocol.objects.create(
            title=f"{protocol.title} (Copy)",
            description=protocol.description,
            author=request.user,
            is_public=False,
            tags=protocol.tags
        )
        
        # Copy steps
        for step in protocol.steps.all():
            ProtocolStep.objects.create(
                protocol=new_protocol,
                step_number=step.step_number,
                step_type=step.step_type,
                title=step.title,
                content=step.content,
                duration_minutes=step.duration_minutes,
                temperature_celsius=step.temperature_celsius,
                reasoning=step.reasoning,
                alternatives=step.alternatives
            )
        
        # Copy reagents
        for reagent in protocol.reagents.all():
            Reagent.objects.create(
                protocol=new_protocol,
                name=reagent.name,
                concentration=reagent.concentration,
                unit=reagent.unit
            )
        
        response_serializer = ProtocolSerializer(new_protocol)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def cross_reference(self, request, pk=None):
        """Get cross-references for a protocol."""
        protocol = self.get_object()
        service = ProtocolService()
        references = service.cross_reference_papers(protocol)
        
        return Response({'references': references})


class ProtocolStepViewSet(viewsets.ModelViewSet):
    """ViewSet for ProtocolStep CRUD operations."""
    
    queryset = ProtocolStep.objects.all()
    serializer_class = ProtocolStepSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter steps by protocol."""
        protocol_id = self.kwargs.get('protocol_pk')
        if protocol_id:
            return ProtocolStep.objects.filter(protocol_id=protocol_id)
        return ProtocolStep.objects.none()
    
    def perform_create(self, serializer):
        """Set the protocol when creating a step."""
        protocol_id = self.kwargs.get('protocol_pk')
        protocol = get_object_or_404(Protocol, id=protocol_id)
        serializer.save(protocol=protocol)


class ReagentViewSet(viewsets.ModelViewSet):
    """ViewSet for Reagent CRUD operations."""
    
    queryset = Reagent.objects.all()
    serializer_class = ReagentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter reagents by protocol."""
        protocol_id = self.kwargs.get('protocol_pk')
        if protocol_id:
            return Reagent.objects.filter(protocol_id=protocol_id)
        return Reagent.objects.none()
    
    def perform_create(self, serializer):
        """Set the protocol when creating a reagent."""
        protocol_id = self.kwargs.get('protocol_pk')
        protocol = get_object_or_404(Protocol, id=protocol_id)
        serializer.save(protocol=protocol)


class ResearchPaperViewSet(viewsets.ModelViewSet):
    """ViewSet for ResearchPaper CRUD operations."""
    
    queryset = ResearchPaper.objects.all()
    serializer_class = ResearchPaperSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['journal', 'publication_date']
    search_fields = ['title', 'authors', 'abstract', 'keywords']
    ordering_fields = ['uploaded_at', 'publication_date', 'title']
    ordering = ['-uploaded_at']
    
    def get_queryset(self):
        """Filter papers based on user permissions."""
        user = self.request.user
        if user.is_staff:
            return ResearchPaper.objects.all()
        return ResearchPaper.objects.filter(uploaded_by=user)
    
    def perform_create(self, serializer):
        """Set the uploader when creating a paper."""
        serializer.save(uploaded_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def extract_content(self, request, pk=None):
        """Extract content from uploaded PDF."""
        paper = self.get_object()
        
        # TODO: Implement PDF content extraction
        # This would use PyPDF2 or pdfminer to extract text
        
        return Response({'message': 'Content extraction started'})
    
    @action(detail=True, methods=['post'])
    def analyze(self, request, pk=None):
        """Analyze paper content for protocol information."""
        paper = self.get_object()
        
        # TODO: Implement paper analysis
        # This would extract protocol parameters and steps
        
        return Response({'message': 'Analysis completed'})


class ProtocolReferenceViewSet(viewsets.ModelViewSet):
    """ViewSet for ProtocolReference CRUD operations."""
    
    queryset = ProtocolReference.objects.all()
    serializer_class = ProtocolReferenceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter references by protocol."""
        protocol_id = self.kwargs.get('protocol_pk')
        if protocol_id:
            return ProtocolReference.objects.filter(protocol_id=protocol_id)
        return ProtocolReference.objects.none()
    
    def perform_create(self, serializer):
        """Set the protocol when creating a reference."""
        protocol_id = self.kwargs.get('protocol_pk')
        protocol = get_object_or_404(Protocol, id=protocol_id)
        serializer.save(protocol=protocol) 