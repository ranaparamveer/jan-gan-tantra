"""
API integration tests for Wiki endpoints
"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from wiki.models import Category, Solution


class WikiAPITest(TestCase):
    """Test Wiki API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.force_authenticate(user=self.user)
        
        self.category = Category.objects.create(
            name="Sanitation",
            description="Garbage issues"
        )
        self.solution = Solution.objects.create(
            title="How to report garbage",
            description="Step-by-step guide",
            category=self.category,
            language="en",
            steps="1. Find officer\n2. File complaint"
        )
    
    def test_list_categories(self):
        """Test GET /api/wiki/categories/"""
        url = reverse('category-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Sanitation')
    
    def test_list_solutions(self):
        """Test GET /api/wiki/solutions/"""
        url = reverse('solution-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)
    
    def test_search_solutions(self):
        """Test search functionality"""
        url = reverse('solution-list')
        response = self.client.get(url, {'search': 'garbage'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)
    
    def test_filter_by_category(self):
        """Test filtering by category"""
        url = reverse('solution-list')
        response = self.client.get(url, {'category': self.category.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for solution in response.data['results']:
            self.assertEqual(solution['category'], self.category.id)
    
    def test_upvote_solution(self):
        """Test upvoting a solution"""
        url = reverse('solution-upvote', kwargs={'pk': self.solution.id})
        initial_upvotes = self.solution.upvotes
        
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.solution.refresh_from_db()
        self.assertEqual(self.solution.upvotes, initial_upvotes + 1)
    
    def test_create_solution(self):
        """Test creating a new solution"""
        url = reverse('solution-list')
        data = {
            'title': 'New Solution',
            'description': 'Test description',
            'category_id': self.category.id,
            'language': 'en',
            'steps': ['1. Step one', '2. Step two']
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Solution.objects.count(), 2)
