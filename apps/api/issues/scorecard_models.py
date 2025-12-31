"""
Accountability Scorecard Model
Tracks government officer/department performance metrics
"""
from django.db import models
from govgraph.models import Officer, Department


class AccountabilityScore(models.Model):
    """
    Performance scorecard for officers and departments
    """
    
    # Link to officer or department
    officer = models.ForeignKey(
        Officer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='scorecards'
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='scorecards'
    )
    
    # Metrics
    total_issues_assigned = models.IntegerField(default=0)
    issues_resolved = models.IntegerField(default=0)
    issues_pending = models.IntegerField(default=0)
    issues_overdue = models.IntegerField(default=0)
    
    # Performance indicators
    avg_resolution_time_days = models.FloatField(default=0.0)
    citizen_satisfaction_score = models.FloatField(default=0.0)  # 0-5 scale
    response_rate = models.FloatField(default=0.0)  # Percentage
    
    # Accountability metrics
    sla_compliance_rate = models.FloatField(default=0.0)  # Percentage
    escalation_count = models.IntegerField(default=0)
    
    # Timestamps
    period_start = models.DateField()
    period_end = models.DateField()
    calculated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-calculated_at']
        indexes = [
            models.Index(fields=['officer', '-calculated_at']),
            models.Index(fields=['department', '-calculated_at']),
        ]
    
    def __str__(self):
        if self.officer:
            return f"Scorecard: {self.officer.name} ({self.period_start} to {self.period_end})"
        return f"Scorecard: {self.department.name} ({self.period_start} to {self.period_end})"
    
    @property
    def resolution_rate(self):
        """Calculate resolution rate percentage"""
        if self.total_issues_assigned == 0:
            return 0.0
        return (self.issues_resolved / self.total_issues_assigned) * 100
    
    @property
    def overall_score(self):
        """
        Calculate overall accountability score (0-100)
        Weighted average of key metrics
        """
        weights = {
            'resolution_rate': 0.3,
            'sla_compliance': 0.25,
            'response_rate': 0.2,
            'satisfaction': 0.15,
            'speed': 0.1,
        }
        
        # Normalize metrics to 0-100 scale
        resolution = self.resolution_rate
        sla = self.sla_compliance_rate
        response = self.response_rate
        satisfaction = (self.citizen_satisfaction_score / 5.0) * 100
        
        # Speed score (inverse of avg resolution time, capped at 30 days)
        speed = max(0, (30 - self.avg_resolution_time_days) / 30 * 100)
        
        score = (
            resolution * weights['resolution_rate'] +
            sla * weights['sla_compliance'] +
            response * weights['response_rate'] +
            satisfaction * weights['satisfaction'] +
            speed * weights['speed']
        )
        
        return round(score, 2)
    
    @property
    def grade(self):
        """Get letter grade based on overall score"""
        score = self.overall_score
        if score >= 90:
            return 'A+'
        elif score >= 80:
            return 'A'
        elif score >= 70:
            return 'B'
        elif score >= 60:
            return 'C'
        elif score >= 50:
            return 'D'
        else:
            return 'F'


class CitizenFeedback(models.Model):
    """
    Citizen feedback on issue resolution
    """
    
    issue = models.ForeignKey(
        'issues.Issue',
        on_delete=models.CASCADE,
        related_name='feedback'
    )
    officer = models.ForeignKey(
        Officer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # Ratings (1-5 scale)
    responsiveness_rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],
        help_text="How quickly did they respond?"
    )
    helpfulness_rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],
        help_text="How helpful were they?"
    )
    resolution_rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],
        help_text="How satisfied are you with the resolution?"
    )
    
    # Comments
    comment = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Feedback for Issue #{self.issue.id}"
    
    @property
    def average_rating(self):
        """Calculate average rating across all dimensions"""
        return (
            self.responsiveness_rating +
            self.helpfulness_rating +
            self.resolution_rating
        ) / 3.0
