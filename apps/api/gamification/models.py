"""
Gamification system for crowdsourcing
Rewards users for contributing data and verifying information
"""
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Extended user profile with gamification metrics
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Points and levels
    points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    
    # Contribution stats
    solutions_contributed = models.IntegerField(default=0)
    issues_reported = models.IntegerField(default=0)
    verifications_done = models.IntegerField(default=0)
    translations_contributed = models.IntegerField(default=0)
    
    # Badges
    badges = models.JSONField(default=list)
    
    # Reputation
    reputation_score = models.FloatField(default=0.0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-points']
    
    def __str__(self):
        return f"{self.user.username} - Level {self.level} ({self.points} points)"
    
    def add_points(self, points, activity_type):
        """
        Add points for an activity
        
        Args:
            points: Points to add
            activity_type: Type of activity (for tracking)
        """
        self.points += points
        
        # Check for level up
        new_level = self._calculate_level()
        if new_level > self.level:
            self.level = new_level
            self._award_level_badge(new_level)
        
        self.save()
        
        # Log activity
        ActivityLog.objects.create(
            user_profile=self,
            activity_type=activity_type,
            points_earned=points
        )
    
    def _calculate_level(self):
        """Calculate level based on points (100 points per level)"""
        return (self.points // 100) + 1
    
    def _award_level_badge(self, level):
        """Award badge for reaching a new level"""
        badge = f"Level {level} Achiever"
        if badge not in self.badges:
            self.badges.append(badge)
    
    def award_badge(self, badge_name):
        """Award a special badge"""
        if badge_name not in self.badges:
            self.badges.append(badge_name)
            self.save()


class ActivityLog(models.Model):
    """
    Log of user activities for gamification
    """
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=50)
    points_earned = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user_profile.user.username} - {self.activity_type} (+{self.points_earned})"


class Leaderboard(models.Model):
    """
    Weekly/monthly leaderboard
    """
    PERIOD_CHOICES = [
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('all_time', 'All Time'),
    ]
    
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    period_type = models.CharField(max_length=20, choices=PERIOD_CHOICES)
    period_start = models.DateField()
    period_end = models.DateField()
    rank = models.IntegerField()
    points_in_period = models.IntegerField()
    
    class Meta:
        ordering = ['period_type', 'rank']
        unique_together = ['user_profile', 'period_type', 'period_start']
    
    def __str__(self):
        return f"{self.period_type} - Rank {self.rank}: {self.user_profile.user.username}"


# Point values for different activities
ACTIVITY_POINTS = {
    'solution_contributed': 50,
    'issue_reported': 10,
    'issue_resolved': 30,
    'contact_verified': 20,
    'translation_contributed': 15,
    'upvote_received': 5,
    'success_path_shared': 40,
}

# Special badges
BADGES = {
    'first_contribution': 'First Contribution',
    'verified_contributor': 'Verified Contributor',
    'super_reporter': 'Super Reporter (100+ issues)',
    'solution_master': 'Solution Master (50+ solutions)',
    'translation_hero': 'Translation Hero (100+ translations)',
    'community_champion': 'Community Champion',
}
