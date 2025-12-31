"""
Unit tests for Wiki module
"""
from django.test import TestCase
from django.contrib.auth.models import User
from wiki.models import Category, Solution, Template, SuccessPath


class CategoryModelTest(TestCase):
    """Test Category model"""
    
    def setUp(self):
        self.category = Category.objects.create(
            name="Sanitation",
            description="Garbage and sewage issues"
        )
    
    def test_category_creation(self):
        """Test category is created correctly"""
        self.assertEqual(self.category.name, "Sanitation")
        self.assertIsNotNone(self.category.created_at)
    
    def test_category_str(self):
        """Test string representation"""
        self.assertEqual(str(self.category), "Sanitation")


class SolutionModelTest(TestCase):
    """Test Solution model"""
    
    def setUp(self):
        self.category = Category.objects.create(name="Sanitation")
        self.solution = Solution.objects.create(
            title="How to report garbage collection issues",
            description="Step-by-step guide",
            category=self.category,
            language="en",
            steps="1. Find officer\n2. File complaint\n3. Follow up"
        )
    
    def test_solution_creation(self):
        """Test solution is created correctly"""
        self.assertEqual(self.solution.title, "How to report garbage collection issues")
        self.assertEqual(self.solution.upvotes, 0)
        self.assertFalse(self.solution.is_verified)
    
    def test_solution_upvote(self):
        """Test upvoting a solution"""
        initial_upvotes = self.solution.upvotes
        self.solution.upvotes += 1
        self.solution.save()
        self.assertEqual(self.solution.upvotes, initial_upvotes + 1)
    
    def test_success_rate_default(self):
        """Test default success rate"""
        self.assertEqual(self.solution.success_rate, 0.0)


class TemplateModelTest(TestCase):
    """Test Template model"""
    
    def setUp(self):
        self.template = Template.objects.create(
            name="RTI Application",
            template_type="rti",
            language="en",
            content="To,\nPublic Information Officer\n..."
        )
    
    def test_template_creation(self):
        """Test template is created correctly"""
        self.assertEqual(self.template.name, "RTI Application")
        self.assertEqual(self.template.template_type, "rti")
    
    def test_template_str(self):
        """Test string representation"""
        self.assertEqual(str(self.template), "RTI Application (rti)")


class SuccessPathModelTest(TestCase):
    """Test SuccessPath model"""
    
    def setUp(self):
        category = Category.objects.create(name="Sanitation")
        self.solution = Solution.objects.create(
            title="Test Solution",
            category=category,
            language="en"
        )
        self.success_path = SuccessPath.objects.create(
            solution=self.solution,
            user_name="John Doe",
            story="I followed the steps and it worked!",
            resolution_time_days=7
        )
    
    def test_success_path_creation(self):
        """Test success path is created correctly"""
        self.assertEqual(self.success_path.user_name, "John Doe")
        self.assertEqual(self.success_path.resolution_time_days, 7)
    
    def test_success_path_relationship(self):
        """Test relationship with solution"""
        self.assertEqual(self.success_path.solution, self.solution)
        self.assertEqual(self.solution.success_paths.count(), 1)
