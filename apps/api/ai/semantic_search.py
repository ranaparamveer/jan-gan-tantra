"""
Semantic Search Service using pgvector
Enables intelligent search across solutions and issues
"""
from sentence_transformers import SentenceTransformer
import numpy as np
from django.db import connection


class SemanticSearchService:
    """
    Semantic search using sentence embeddings and pgvector
    """
    
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """
        Initialize with a sentence transformer model
        
        Args:
            model_name: HuggingFace model name (default: lightweight multilingual model)
        """
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = 384  # Dimension for all-MiniLM-L6-v2
    
    def generate_embedding(self, text):
        """
        Generate vector embedding for text
        
        Args:
            text: Input text string
        
        Returns:
            numpy array of embedding vector
        """
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding
    
    def search_solutions(self, query, limit=10, threshold=0.7):
        """
        Semantic search for solutions
        
        Args:
            query: Search query string
            limit: Maximum number of results
            threshold: Minimum similarity threshold (0-1)
        
        Returns:
            List of (solution_id, title, similarity_score) tuples
        """
        # Generate query embedding
        query_embedding = self.generate_embedding(query)
        
        # Convert to PostgreSQL vector format
        vector_str = '[' + ','.join(map(str, query_embedding)) + ']'
        
        # Perform similarity search using pgvector
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    id,
                    title,
                    description,
                    1 - (embedding <=> %s::vector) as similarity
                FROM wiki_solution
                WHERE embedding IS NOT NULL
                    AND 1 - (embedding <=> %s::vector) > %s
                ORDER BY embedding <=> %s::vector
                LIMIT %s
            """, [vector_str, vector_str, threshold, vector_str, limit])
            
            results = cursor.fetchall()
        
        return [
            {
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'similarity': float(row[3])
            }
            for row in results
        ]
    
    def search_issues(self, query, limit=10, threshold=0.7):
        """
        Semantic search for issues
        
        Args:
            query: Search query string
            limit: Maximum number of results
            threshold: Minimum similarity threshold (0-1)
        
        Returns:
            List of issue dictionaries with similarity scores
        """
        query_embedding = self.generate_embedding(query)
        vector_str = '[' + ','.join(map(str, query_embedding)) + ']'
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    id,
                    title,
                    description,
                    status,
                    1 - (embedding <=> %s::vector) as similarity
                FROM issues_issue
                WHERE embedding IS NOT NULL
                    AND 1 - (embedding <=> %s::vector) > %s
                ORDER BY embedding <=> %s::vector
                LIMIT %s
            """, [vector_str, vector_str, threshold, vector_str, limit])
            
            results = cursor.fetchall()
        
        return [
            {
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'status': row[3],
                'similarity': float(row[4])
            }
            for row in results
        ]
    
    def find_similar_solutions(self, solution_id, limit=5):
        """
        Find solutions similar to a given solution
        
        Args:
            solution_id: ID of the reference solution
            limit: Maximum number of similar solutions
        
        Returns:
            List of similar solution dictionaries
        """
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    s2.id,
                    s2.title,
                    s2.description,
                    1 - (s1.embedding <=> s2.embedding) as similarity
                FROM wiki_solution s1
                CROSS JOIN wiki_solution s2
                WHERE s1.id = %s
                    AND s2.id != %s
                    AND s1.embedding IS NOT NULL
                    AND s2.embedding IS NOT NULL
                ORDER BY s1.embedding <=> s2.embedding
                LIMIT %s
            """, [solution_id, solution_id, limit])
            
            results = cursor.fetchall()
        
        return [
            {
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'similarity': float(row[3])
            }
            for row in results
        ]
    
    def cluster_similar_issues(self, min_similarity=0.8):
        """
        Find clusters of similar issues for collective action
        
        Args:
            min_similarity: Minimum similarity to consider issues related
        
        Returns:
            List of issue clusters
        """
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    i1.id as issue1_id,
                    i2.id as issue2_id,
                    i1.title as issue1_title,
                    i2.title as issue2_title,
                    1 - (i1.embedding <=> i2.embedding) as similarity
                FROM issues_issue i1
                CROSS JOIN issues_issue i2
                WHERE i1.id < i2.id
                    AND i1.embedding IS NOT NULL
                    AND i2.embedding IS NOT NULL
                    AND 1 - (i1.embedding <=> i2.embedding) > %s
                    AND i1.status = 'reported'
                    AND i2.status = 'reported'
                ORDER BY similarity DESC
            """, [min_similarity])
            
            results = cursor.fetchall()
        
        # Group into clusters
        clusters = {}
        for row in results:
            issue1_id, issue2_id = row[0], row[1]
            similarity = float(row[4])
            
            # Find existing cluster or create new one
            cluster_key = None
            for key, cluster in clusters.items():
                if issue1_id in cluster['issue_ids'] or issue2_id in cluster['issue_ids']:
                    cluster_key = key
                    break
            
            if cluster_key:
                clusters[cluster_key]['issue_ids'].update([issue1_id, issue2_id])
                clusters[cluster_key]['avg_similarity'] = (
                    clusters[cluster_key]['avg_similarity'] + similarity
                ) / 2
            else:
                clusters[len(clusters)] = {
                    'issue_ids': {issue1_id, issue2_id},
                    'avg_similarity': similarity
                }
        
        return [
            {
                'issue_ids': list(cluster['issue_ids']),
                'count': len(cluster['issue_ids']),
                'avg_similarity': cluster['avg_similarity']
            }
            for cluster in clusters.values()
        ]


# Singleton instance
_search_service = None

def get_search_service():
    """Get or create semantic search service instance"""
    global _search_service
    if _search_service is None:
        _search_service = SemanticSearchService()
    return _search_service
