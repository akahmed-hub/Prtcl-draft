import json
import logging
from typing import List, Dict, Any, Optional
from django.conf import settings
from django.utils import timezone
from .models import Protocol, ProtocolStep, Reagent, ResearchPaper
import anthropic

logger = logging.getLogger(__name__)


class LLMService:
    """Service for interacting with LLM APIs."""
    
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    def generate_protocol(self, prompt: str, include_reagents: bool = True, 
                         include_reasoning: bool = True, max_steps: int = 20) -> Dict[str, Any]:
        """
        Generate a protocol using the LLM.
        
        Args:
            prompt: User's protocol request
            include_reagents: Whether to include reagent information
            include_reasoning: Whether to include reasoning for each step
            max_steps: Maximum number of steps to generate
            
        Returns:
            Dictionary containing generated protocol data
        """
        try:
            # Construct the system prompt
            system_prompt = self._build_system_prompt(include_reagents, include_reasoning, max_steps)
            
            # Generate protocol using Claude
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Parse the response
            content = response.content[0].text
            protocol_data = self._parse_llm_response(content)
            
            return protocol_data
            
        except Exception as e:
            logger.error(f"Error generating protocol: {str(e)}")
            raise
    
    def _build_system_prompt(self, include_reagents: bool, include_reasoning: bool, max_steps: int) -> str:
        """Build the system prompt for protocol generation."""
        prompt = f"""You are an expert in biological research protocols. Generate a detailed protocol based on the user's request.

Requirements:
- Maximum {max_steps} steps
- Each step should be concise but informative
- Include specific parameters (temperatures, times, concentrations) when relevant
- Use clear, action-oriented language

Output Format (JSON):
{{
    "title": "Protocol Title",
    "description": "Brief description",
    "reagents": [
        {{
            "name": "Reagent Name",
            "concentration": "Concentration",
            "unit": "Unit"
        }}
    ],
    "steps": [
        {{
            "step_number": 1,
            "title": "Step Title",
            "content": "Detailed step description",
            "duration_minutes": 30,
            "temperature_celsius": 37.0,
            "reasoning": "Why this step is performed",
            "alternatives": [
                {{
                    "parameter": "temperature",
                    "value": "42°C",
                    "source": "Paper reference",
                    "reason": "Alternative approach"
                }}
            ]
        }}
    ]
}}

Guidelines:
- If include_reagents is true, list all reagents at the top
- If include_reasoning is true, provide reasoning for each step
- Include alternatives when there are conflicting parameters from different sources
- Be specific about concentrations, temperatures, and times
- Use standard biological terminology"""
        
        return prompt
    
    def _parse_llm_response(self, content: str) -> Dict[str, Any]:
        """Parse the LLM response into structured data."""
        try:
            # Try to extract JSON from the response
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON found in response")
            
            json_str = content[start_idx:end_idx]
            data = json.loads(json_str)
            
            # Validate required fields
            required_fields = ['title', 'steps']
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Missing required field: {field}")
            
            return data
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            # Fallback: create a basic structure
            return {
                'title': 'Generated Protocol',
                'description': content[:200] + '...' if len(content) > 200 else content,
                'reagents': [],
                'steps': []
            }


class ProtocolService:
    """Service for protocol-related operations."""
    
    def __init__(self):
        self.llm_service = LLMService()
    
    def create_protocol_from_prompt(self, user, prompt: str, **kwargs) -> Protocol:
        """
        Create a new protocol from a user prompt.
        
        Args:
            user: The user creating the protocol
            prompt: The user's protocol request
            **kwargs: Additional options for protocol generation
            
        Returns:
            The created Protocol instance
        """
        # Generate protocol using LLM
        protocol_data = self.llm_service.generate_protocol(prompt, **kwargs)
        
        # Create protocol in database
        protocol = Protocol.objects.create(
            author=user,
            title=protocol_data.get('title', 'Generated Protocol'),
            description=protocol_data.get('description', ''),
            original_prompt=prompt,
            llm_model_used='claude-3-sonnet-20240229',
            generation_timestamp=timezone.now()
        )
        
        # Create reagents
        for reagent_data in protocol_data.get('reagents', []):
            Reagent.objects.create(
                protocol=protocol,
                name=reagent_data.get('name', ''),
                concentration=reagent_data.get('concentration', ''),
                unit=reagent_data.get('unit', '')
            )
        
        # Create steps
        for step_data in protocol_data.get('steps', []):
            step = ProtocolStep.objects.create(
                protocol=protocol,
                step_number=step_data.get('step_number', 1),
                title=step_data.get('title', ''),
                content=step_data.get('content', ''),
                duration_minutes=step_data.get('duration_minutes'),
                temperature_celsius=step_data.get('temperature_celsius'),
                reasoning=step_data.get('reasoning', ''),
                alternatives=step_data.get('alternatives', [])
            )
        
        return protocol
    
    def search_protocols(self, query: str, search_type: str = 'keyword', 
                        filters: Dict[str, Any] = None, limit: int = 20) -> List[Protocol]:
        """
        Search for protocols based on query and filters.
        
        Args:
            query: Search query
            search_type: Type of search ('keyword', 'semantic', 'both')
            filters: Additional filters
            limit: Maximum number of results
            
        Returns:
            List of matching protocols
        """
        queryset = Protocol.objects.all()
        
        # Apply filters
        if filters:
            if 'author' in filters:
                queryset = queryset.filter(author__username__icontains=filters['author'])
            if 'tags' in filters:
                queryset = queryset.filter(tags__contains=filters['tags'])
            if 'is_public' in filters:
                queryset = queryset.filter(is_public=filters['is_public'])
        
        # Apply search
        if search_type in ['keyword', 'both']:
            from django.db import models
            queryset = queryset.filter(
                models.Q(title__icontains=query) |
                models.Q(description__icontains=query) |
                models.Q(original_prompt__icontains=query) |
                models.Q(steps__content__icontains=query)
            ).distinct()
        
        # TODO: Implement semantic search when needed
        if search_type in ['semantic', 'both']:
            # Placeholder for semantic search implementation
            pass
        
        return queryset[:limit]
    
    def cross_reference_papers(self, protocol: Protocol) -> List[Dict[str, Any]]:
        """
        Cross-reference protocol with research papers.
        
        Args:
            protocol: The protocol to cross-reference
            
        Returns:
            List of relevant papers and their references
        """
        # TODO: Implement paper cross-referencing logic
        # This would involve:
        # 1. Searching papers database for relevant protocols
        # 2. Comparing parameters and steps
        # 3. Identifying conflicts and alternatives
        
        return []
    
    def extract_protocol_parameters(self, text: str) -> Dict[str, Any]:
        """
        Extract protocol parameters from text using NLP.
        
        Args:
            text: Text to extract parameters from
            
        Returns:
            Dictionary of extracted parameters
        """
        # TODO: Implement parameter extraction using regex/NLP
        # This would extract temperatures, times, concentrations, etc.
        
        parameters = {
            'temperatures': [],
            'times': [],
            'concentrations': [],
            'reagents': []
        }
        
        return parameters 