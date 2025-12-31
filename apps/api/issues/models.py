from django.contrib.gis.db import models
from django.contrib.auth.models import User


class Issue(models.Model):
    """
    User-reported civic issues with geolocation
    """
    STATUS_CHOICES = [
        ('reported', 'Reported'),
        ('acknowledged', 'Acknowledged'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey('wiki.Category', on_delete=models.CASCADE, related_name='issues')
    
    # Geospatial data
    location = models.PointField(help_text="Geographic coordinates")
    address = models.TextField(blank=True)
    
    # Status tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reported')
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reported_issues')
    assigned_to = models.ForeignKey('govgraph.Officer', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Evidence
    evidence_photos = models.JSONField(default=list, help_text="URLs to uploaded photos")
    evidence_documents = models.JSONField(default=list, help_text="URLs to uploaded documents")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    # Engagement metrics
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'category']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"


class IssueUpdate(models.Model):
    """
    Status updates on issues
    """
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='updates')
    message = models.TextField()
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']


class IssueCluster(models.Model):
    """
    Detected clusters of similar issues in a geographic area
    """
    category = models.ForeignKey('wiki.Category', on_delete=models.CASCADE)
    center_point = models.PointField(help_text="Cluster centroid")
    radius_meters = models.FloatField(help_text="Cluster radius")
    issue_count = models.IntegerField()
    severity_score = models.FloatField(help_text="Calculated based on count and duration")
    
    # Auto-generated petition
    petition_text = models.TextField(blank=True)
    petition_signed_by = models.ManyToManyField(User, related_name='signed_petitions', blank=True)
    
    detected_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-severity_score', '-detected_at']
    
    def __str__(self):
        return f"Cluster: {self.category.name} ({self.issue_count} issues)"
