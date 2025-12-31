from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Department, Designation, Officer, ContactVerification
from .serializers import (
    DepartmentSerializer,
    DesignationSerializer,
    OfficerSerializer,
    ContactVerificationSerializer,
    EscalationLadderSerializer
)


class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Browse government department hierarchy
    """
    queryset = Department.objects.select_related('parent')
    serializer_class = DepartmentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'state', 'district', 'city']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by level
        level = self.request.query_params.get('level')
        if level:
            queryset = queryset.filter(level=level)
        
        # Filter by location
        state = self.request.query_params.get('state')
        if state:
            queryset = queryset.filter(state__iexact=state)
        
        district = self.request.query_params.get('district')
        if district:
            queryset = queryset.filter(district__iexact=district)
        
        city = self.request.query_params.get('city')
        if city:
            queryset = queryset.filter(city__iexact=city)
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def hierarchy(self, request, pk=None):
        """
        Get full hierarchy from this department up to central government
        """
        department = self.get_object()
        hierarchy = []
        current = department
        
        while current:
            hierarchy.insert(0, DepartmentSerializer(current).data)
            current = current.parent
        
        return Response(hierarchy)


class DesignationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Browse official designations
    """
    queryset = Designation.objects.select_related('department').prefetch_related('officers')
    serializer_class = DesignationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'department__name']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by department
        department_id = self.request.query_params.get('department')
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        
        return queryset


class OfficerViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for government officers
    """
    queryset = Officer.objects.select_related('designation__department')
    serializer_class = OfficerSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'designation__title', 'designation__department__name']
    ordering_fields = ['verified_by_users', 'created_at']
    ordering = ['-is_active', '-verified_by_users']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter active only
        active_only = self.request.query_params.get('active')
        if active_only == 'true':
            queryset = queryset.filter(is_active=True)
        
        # Filter by designation
        designation_id = self.request.query_params.get('designation')
        if designation_id:
            queryset = queryset.filter(designation_id=designation_id)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """
        Verify officer contact details
        """
        officer = self.get_object()
        is_correct = request.data.get('is_correct', True)
        notes = request.data.get('notes', '')
        
        # Create verification record
        ContactVerification.objects.create(
            officer=officer,
            verified_by=request.user,
            is_correct=is_correct,
            notes=notes
        )
        
        # Update officer verification count
        if is_correct:
            officer.verified_by_users += 1
            officer.last_verified_at = timezone.now()
            officer.save()
        
        return Response({
            'verified_by_users': officer.verified_by_users,
            'last_verified_at': officer.last_verified_at
        })
    
    @action(detail=False, methods=['get'])
    def find_responsible(self, request):
        """
        Find responsible officer for a given issue category and location
        """
        category = request.query_params.get('category')
        state = request.query_params.get('state')
        district = request.query_params.get('district')
        city = request.query_params.get('city')
        
        # TODO: Implement smart matching logic based on category and location
        # For now, return a simple query
        queryset = self.get_queryset().filter(is_active=True)
        
        if state:
            queryset = queryset.filter(designation__department__state__iexact=state)
        if district:
            queryset = queryset.filter(designation__department__district__iexact=district)
        if city:
            queryset = queryset.filter(designation__department__city__iexact=city)
        
        officers = queryset[:5]  # Return top 5 matches
        serializer = self.get_serializer(officers, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def escalation_ladder(self, request, pk=None):
        """
        Get escalation ladder starting from this officer
        """
        officer = self.get_object()
        department = officer.designation.department
        
        # Get all designations in this department, ordered by level
        designations = Designation.objects.filter(
            department=department
        ).order_by('level').select_related('department')
        
        ladder = []
        for designation in designations:
            current_officer = designation.officers.filter(is_active=True).first()
            ladder.append({
                'level': designation.level,
                'designation': DesignationSerializer(designation).data,
                'officer': OfficerSerializer(current_officer).data if current_officer else None
            })
        
        return Response(ladder)


class ContactVerificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    View contact verification history
    """
    queryset = ContactVerification.objects.select_related('officer', 'verified_by')
    serializer_class = ContactVerificationSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by officer
        officer_id = self.request.query_params.get('officer')
        if officer_id:
            queryset = queryset.filter(officer_id=officer_id)
        
        return queryset
