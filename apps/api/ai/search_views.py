from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .semantic_search import get_search_service


class SemanticSearchView(APIView):
    """
    Semantic search across solutions and issues using AI embeddings
    """
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'query',
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description='Search query'
            ),
            openapi.Parameter(
                'type',
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=False,
                description='Search type: solutions or issues (default: solutions)'
            ),
            openapi.Parameter(
                'limit',
                openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=False,
                description='Maximum results (default: 10)'
            ),
        ],
        responses={200: 'List of search results with similarity scores'}
    )
    def get(self, request):
        query = request.query_params.get('query')
        search_type = request.query_params.get('type', 'solutions')
        limit = int(request.query_params.get('limit', 10))
        
        if not query:
            return Response(
                {'error': 'query parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            search_service = get_search_service()
            
            if search_type == 'solutions':
                results = search_service.search_solutions(query, limit=limit)
            elif search_type == 'issues':
                results = search_service.search_issues(query, limit=limit)
            else:
                return Response(
                    {'error': 'Invalid search type. Use "solutions" or "issues"'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            return Response({
                'query': query,
                'type': search_type,
                'count': len(results),
                'results': results
            })
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SimilarSolutionsView(APIView):
    """
    Find solutions similar to a given solution
    """
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'solution_id',
                openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                required=True,
                description='Solution ID'
            ),
            openapi.Parameter(
                'limit',
                openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=False,
                description='Maximum results (default: 5)'
            ),
        ],
        responses={200: 'List of similar solutions'}
    )
    def get(self, request, solution_id):
        limit = int(request.query_params.get('limit', 5))
        
        try:
            search_service = get_search_service()
            results = search_service.find_similar_solutions(solution_id, limit=limit)
            
            return Response({
                'solution_id': solution_id,
                'count': len(results),
                'similar_solutions': results
            })
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class IssueClustersView(APIView):
    """
    Find clusters of similar issues for collective action
    """
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'min_similarity',
                openapi.IN_QUERY,
                type=openapi.TYPE_NUMBER,
                required=False,
                description='Minimum similarity threshold (0-1, default: 0.8)'
            ),
        ],
        responses={200: 'List of issue clusters'}
    )
    def get(self, request):
        min_similarity = float(request.query_params.get('min_similarity', 0.8))
        
        try:
            search_service = get_search_service()
            clusters = search_service.cluster_similar_issues(min_similarity=min_similarity)
            
            return Response({
                'min_similarity': min_similarity,
                'cluster_count': len(clusters),
                'clusters': clusters
            })
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
