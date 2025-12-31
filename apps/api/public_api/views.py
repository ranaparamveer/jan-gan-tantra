"""
Public API for Journalists and Activists
Provides access to civic data for investigative reporting and research
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import timedelta

from issues.models import Issue
from govgraph.models import Department, Officer
from wiki.models import Solution


class PublicDataRateThrottle(UserRateThrottle):
    """Rate limiting for public API - 100 requests per hour"""
    rate = '100/hour'


class IssueStatisticsView(APIView):
    """
    Get aggregated issue statistics by region, category, and time period
    For investigative journalism and research
    """
    throttle_classes = [PublicDataRateThrottle]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'region',
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Filter by region/city'
            ),
            openapi.Parameter(
                'category',
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Filter by category'
            ),
            openapi.Parameter(
                'start_date',
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Start date (YYYY-MM-DD)'
            ),
            openapi.Parameter(
                'end_date',
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='End date (YYYY-MM-DD)'
            ),
        ],
        responses={200: 'Aggregated issue statistics'}
    )
    def get(self, request):
        # Base queryset
        queryset = Issue.objects.all()
        
        # Apply filters
        region = request.query_params.get('region')
        category = request.query_params.get('category')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if region:
            queryset = queryset.filter(location__icontains=region)
        if category:
            queryset = queryset.filter(category__name=category)
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        
        # Calculate statistics
        total_issues = queryset.count()
        
        by_status = queryset.values('status').annotate(count=Count('id'))
        by_category = queryset.values('category__name').annotate(count=Count('id'))
        
        resolved_issues = queryset.filter(status='resolved').count()
        resolution_rate = (resolved_issues / total_issues * 100) if total_issues > 0 else 0
        
        # Average resolution time for resolved issues
        resolved_with_time = queryset.filter(
            status='resolved',
            resolved_at__isnull=False
        )
        
        avg_resolution_days = None
        if resolved_with_time.exists():
            resolution_times = [
                (issue.resolved_at - issue.created_at).days
                for issue in resolved_with_time
            ]
            avg_resolution_days = sum(resolution_times) / len(resolution_times)
        
        return Response({
            'total_issues': total_issues,
            'resolution_rate': round(resolution_rate, 2),
            'avg_resolution_days': round(avg_resolution_days, 2) if avg_resolution_days else None,
            'by_status': list(by_status),
            'by_category': list(by_category),
            'filters_applied': {
                'region': region,
                'category': category,
                'start_date': start_date,
                'end_date': end_date,
            }
        })


class DepartmentPerformanceView(APIView):
    """
    Get department performance metrics
    For accountability reporting
    """
    throttle_classes = [PublicDataRateThrottle]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'department_id',
                openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='Filter by department ID'
            ),
            openapi.Parameter(
                'min_issues',
                openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='Minimum issues to include department (default: 10)'
            ),
        ],
        responses={200: 'Department performance metrics'}
    )
    def get(self, request):
        min_issues = int(request.query_params.get('min_issues', 10))
        department_id = request.query_params.get('department_id')
        
        # Get departments with issue counts
        departments = Department.objects.annotate(
            total_issues=Count('officers__issues')
        ).filter(total_issues__gte=min_issues)
        
        if department_id:
            departments = departments.filter(id=department_id)
        
        results = []
        for dept in departments:
            # Get issues for this department
            dept_issues = Issue.objects.filter(
                assigned_officer__designation__department=dept
            )
            
            total = dept_issues.count()
            resolved = dept_issues.filter(status='resolved').count()
            pending = dept_issues.filter(status='reported').count()
            
            resolution_rate = (resolved / total * 100) if total > 0 else 0
            
            results.append({
                'department_id': dept.id,
                'department_name': dept.name,
                'total_issues': total,
                'resolved_issues': resolved,
                'pending_issues': pending,
                'resolution_rate': round(resolution_rate, 2),
            })
        
        # Sort by resolution rate
        results.sort(key=lambda x: x['resolution_rate'], reverse=True)
        
        return Response({
            'departments': results,
            'count': len(results)
        })


class TrendAnalysisView(APIView):
    """
    Get trend data for time-series analysis
    For data journalism and visualization
    """
    throttle_classes = [PublicDataRateThrottle]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'metric',
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Metric to analyze: issues, solutions, verifications',
                required=True
            ),
            openapi.Parameter(
                'period',
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Time period: daily, weekly, monthly',
                required=True
            ),
            openapi.Parameter(
                'days',
                openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='Number of days to look back (default: 30)'
            ),
        ],
        responses={200: 'Trend data points'}
    )
    def get(self, request):
        metric = request.query_params.get('metric')
        period = request.query_params.get('period', 'daily')
        days = int(request.query_params.get('days', 30))
        
        if not metric:
            return Response(
                {'error': 'metric parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)
        
        # Get data based on metric
        if metric == 'issues':
            queryset = Issue.objects.filter(
                created_at__gte=start_date,
                created_at__lte=end_date
            )
            
            if period == 'daily':
                data = queryset.extra(
                    select={'date': 'DATE(created_at)'}
                ).values('date').annotate(count=Count('id')).order_by('date')
            else:
                # Simplified weekly/monthly aggregation
                data = [{'date': str(end_date.date()), 'count': queryset.count()}]
        
        elif metric == 'solutions':
            queryset = Solution.objects.filter(
                created_at__gte=start_date,
                created_at__lte=end_date
            )
            
            if period == 'daily':
                data = queryset.extra(
                    select={'date': 'DATE(created_at)'}
                ).values('date').annotate(count=Count('id')).order_by('date')
            else:
                data = [{'date': str(end_date.date()), 'count': queryset.count()}]
        
        else:
            return Response(
                {'error': 'Invalid metric. Use: issues, solutions'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({
            'metric': metric,
            'period': period,
            'start_date': str(start_date.date()),
            'end_date': str(end_date.date()),
            'data_points': list(data)
        })


class DataExportView(APIView):
    """
    Export data in CSV/JSON format for analysis
    Requires authentication
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [PublicDataRateThrottle]
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'dataset',
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Dataset to export: issues, departments, solutions',
                required=True
            ),
            openapi.Parameter(
                'format',
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Export format: json, csv (default: json)'
            ),
            openapi.Parameter(
                'limit',
                openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='Maximum records (default: 1000, max: 10000)'
            ),
        ],
        responses={200: 'Exported data'}
    )
    def get(self, request):
        dataset = request.query_params.get('dataset')
        export_format = request.query_params.get('format', 'json')
        limit = min(int(request.query_params.get('limit', 1000)), 10000)
        
        if not dataset:
            return Response(
                {'error': 'dataset parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get data based on dataset
        if dataset == 'issues':
            queryset = Issue.objects.all()[:limit]
            data = [{
                'id': issue.id,
                'title': issue.title,
                'category': issue.category.name if issue.category else None,
                'status': issue.status,
                'created_at': str(issue.created_at),
                'upvotes': issue.upvotes,
            } for issue in queryset]
        
        elif dataset == 'departments':
            queryset = Department.objects.all()[:limit]
            data = [{
                'id': dept.id,
                'name': dept.name,
                'level': dept.level,
                'officer_count': dept.officers.count(),
            } for dept in queryset]
        
        elif dataset == 'solutions':
            queryset = Solution.objects.all()[:limit]
            data = [{
                'id': sol.id,
                'title': sol.title,
                'category': sol.category.name if sol.category else None,
                'language': sol.language,
                'success_rate': sol.success_rate,
                'upvotes': sol.upvotes,
            } for sol in queryset]
        
        else:
            return Response(
                {'error': 'Invalid dataset. Use: issues, departments, solutions'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({
            'dataset': dataset,
            'format': export_format,
            'count': len(data),
            'data': data
        })
