from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Solution, Category, Template, SuccessPath
from .serializers import (
    SolutionListSerializer, 
    SolutionDetailSerializer,
    CategorySerializer,
    TemplateSerializer,
    SuccessPathSerializer
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and retrieve civic issue categories
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class SolutionViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for civic solutions
    """
    queryset = Solution.objects.select_related('category', 'created_by').prefetch_related('success_paths')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'problem_keywords']
    ordering_fields = ['success_rate', 'created_at']
    ordering = ['-success_rate', '-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return SolutionListSerializer
        return SolutionDetailSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Filter by language
        language = self.request.query_params.get('language', 'en')
        queryset = queryset.filter(language=language)
        
        # Filter verified only
        verified_only = self.request.query_params.get('verified')
        if verified_only == 'true':
            queryset = queryset.filter(is_verified=True)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def upvote(self, request, pk=None):
        """Mark solution as helpful"""
        solution = self.get_object()
        # TODO: Track user votes to prevent duplicates
        solution.success_rate = min(100, solution.success_rate + 1)
        solution.save()
        return Response({'success_rate': solution.success_rate})


class TemplateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Pre-written templates for RTI, complaints, etc.
    """
    queryset = Template.objects.select_related('category')
    serializer_class = TemplateSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by template type
        template_type = self.request.query_params.get('type')
        if template_type:
            queryset = queryset.filter(template_type=template_type)
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Filter by language
        language = self.request.query_params.get('language', 'en')
        queryset = queryset.filter(language=language)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def generate(self, request, pk=None):
        """
        Generate a filled template with user-provided data
        """
        template = self.get_object()
        placeholders = request.data.get('placeholders', {})
        
        # Simple placeholder replacement
        content = template.content
        for key, value in placeholders.items():
            content = content.replace(f'{{{{{key}}}}}', str(value))
        
        return Response({
            'title': template.title,
            'content': content,
            'template_type': template.template_type
        })


class SuccessPathViewSet(viewsets.ModelViewSet):
    """
    User-submitted success stories
    """
    queryset = SuccessPath.objects.select_related('solution', 'user')
    serializer_class = SuccessPathSerializer
    ordering = ['-upvotes', '-created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by solution
        solution_id = self.request.query_params.get('solution')
        if solution_id:
            queryset = queryset.filter(solution_id=solution_id)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def upvote(self, request, pk=None):
        """Upvote a success path"""
        success_path = self.get_object()
        success_path.upvotes += 1
        success_path.save()
        return Response({'upvotes': success_path.upvotes})
