from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django.utils import timezone
from django.db.models import Count, Q
from .models import Issue, IssueUpdate, IssueCluster
from .serializers import (
    IssueListSerializer,
    IssueDetailSerializer,
    IssueUpdateSerializer,
    IssueClusterSerializer
)


class IssueViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for civic issues with geospatial support
    """
    queryset = Issue.objects.select_related('category', 'reported_by', 'assigned_to')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'address']
    ordering_fields = ['created_at', 'upvotes', 'views']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return IssueListSerializer
        return IssueDetailSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by status
        issue_status = self.request.query_params.get('status')
        if issue_status:
            queryset = queryset.filter(status=issue_status)
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Filter by bounding box (for map view)
        bbox = self.request.query_params.get('bbox')
        if bbox:
            try:
                # Format: min_lng,min_lat,max_lng,max_lat
                coords = [float(x) for x in bbox.split(',')]
                if len(coords) == 4:
                    from django.contrib.gis.geos import Polygon
                    bbox_polygon = Polygon.from_bbox(coords)
                    queryset = queryset.filter(location__within=bbox_polygon)
            except (ValueError, TypeError):
                pass
        
        # Filter by proximity to a point
        lat = self.request.query_params.get('lat')
        lng = self.request.query_params.get('lng')
        radius_km = self.request.query_params.get('radius', 5)
        
        if lat and lng:
            try:
                point = Point(float(lng), float(lat), srid=4326)
                queryset = queryset.filter(
                    location__distance_lte=(point, D(km=float(radius_km)))
                ).annotate(
                    distance=Distance('location', point)
                ).order_by('distance')
            except (ValueError, TypeError):
                pass
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(reported_by=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        """Increment view count on retrieve"""
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=['views'])
        return super().retrieve(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'])
    def upvote(self, request, pk=None):
        """Upvote an issue"""
        issue = self.get_object()
        issue.upvotes += 1
        issue.save()
        return Response({'upvotes': issue.upvotes})
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """
        Update issue status with audit trail
        """
        issue = self.get_object()
        new_status = request.data.get('status')
        message = request.data.get('message', '')
        
        if new_status not in dict(Issue.STATUS_CHOICES):
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        old_status = issue.status
        issue.status = new_status
        
        if new_status == 'resolved':
            issue.resolved_at = timezone.now()
        
        issue.save()
        
        # Create update record
        IssueUpdate.objects.create(
            issue=issue,
            message=message,
            updated_by=request.user,
            old_status=old_status,
            new_status=new_status
        )
        
        return Response(IssueDetailSerializer(issue).data)
    
    @action(detail=False, methods=['get'])
    def heatmap(self, request):
        """
        Get aggregated issue counts by location for heatmap
        """
        queryset = self.get_queryset()
        
        # Group by approximate location (grid cells)
        # This is a simplified version - production would use PostGIS clustering
        issues = queryset.values('location').annotate(count=Count('id'))
        
        heatmap_data = []
        for item in issues:
            if item['location']:
                heatmap_data.append({
                    'lat': item['location'].y,
                    'lng': item['location'].x,
                    'intensity': item['count']
                })
        
        return Response(heatmap_data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Get issue statistics
        """
        queryset = self.get_queryset()
        
        stats = {
            'total': queryset.count(),
            'by_status': {},
            'by_category': {}
        }
        
        # Count by status
        for status_choice in Issue.STATUS_CHOICES:
            status_code = status_choice[0]
            stats['by_status'][status_code] = queryset.filter(status=status_code).count()
        
        # Count by category
        category_counts = queryset.values('category__name').annotate(count=Count('id'))
        for item in category_counts:
            stats['by_category'][item['category__name']] = item['count']
        
        return Response(stats)


class IssueClusterViewSet(viewsets.ReadOnlyModelViewSet):
    """
    View detected issue clusters
    """
    queryset = IssueCluster.objects.select_related('category')
    serializer_class = IssueClusterSerializer
    ordering = ['-severity_score', '-detected_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter active only
        active_only = self.request.query_params.get('active')
        if active_only == 'true':
            queryset = queryset.filter(is_active=True)
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def sign_petition(self, request, pk=None):
        """
        Sign the auto-generated petition for this cluster
        """
        cluster = self.get_object()
        cluster.petition_signed_by.add(request.user)
        
        return Response({
            'signature_count': cluster.petition_signed_by.count()
        })
