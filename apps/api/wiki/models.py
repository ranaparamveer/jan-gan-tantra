from django.contrib.gis.db import models
from django.contrib.auth.models import User


class Solution(models.Model):
    """
    Searchable solutions for civic problems
    """
    title = models.CharField(max_length=500)
    description = models.TextField()
    problem_keywords = models.JSONField(default=list, help_text="Keywords for semantic search")
    steps = models.JSONField(default=list, help_text="Ordered list of action steps")
    success_rate = models.FloatField(default=0.0, help_text="Percentage of users who found this helpful")
    upvotes = models.IntegerField(default=0)
    language = models.CharField(max_length=10, default='en')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='solutions')
    location = models.PointField(null=True, blank=True, help_text="Geolocation of the solution scope")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-success_rate', '-created_at']
        indexes = [
            models.Index(fields=['language', 'category']),
        ]
    
    def __str__(self):
        return self.title


class Category(models.Model):
    """
    Categories for civic issues (e.g., Sanitation, Roads, Water)
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Icon name for UI")
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Template(models.Model):
    """
    Pre-written templates for RTI, complaints, etc.
    """
    TEMPLATE_TYPES = [
        ('rti', 'RTI Application'),
        ('complaint', 'Formal Complaint'),
        ('appeal', 'First Appeal'),
        ('letter', 'Official Letter'),
    ]
    
    title = models.CharField(max_length=200)
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPES)
    content = models.TextField(help_text="Template with {{placeholders}}")
    language = models.CharField(max_length=10, default='en')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='templates')
    
    class Meta:
        ordering = ['template_type', 'title']
    
    def __str__(self):
        return f"{self.get_template_type_display()} - {self.title}"


class SuccessPath(models.Model):
    """
    User-submitted success stories
    """
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, related_name='success_paths')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    steps_taken = models.JSONField(help_text="Actual steps the user followed")
    outcome = models.TextField()
    time_to_resolve = models.IntegerField(help_text="Days taken to resolve")
    evidence_urls = models.JSONField(default=list, help_text="Links to photos/documents")
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-upvotes', '-created_at']
    
    def __str__(self):
        return f"Success: {self.solution.title}"


class SolutionSuggestion(models.Model):
    """
    User-submitted suggestions/edits for solutions
    """
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, related_name='suggestions')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    suggestion_text = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Suggestion for: {self.solution.title}"
