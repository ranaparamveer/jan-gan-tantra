from django.db import models


class Department(models.Model):
    """
    Government departments at various levels
    """
    LEVELS = [
        ('central', 'Central Government'),
        ('state', 'State Government'),
        ('district', 'District Administration'),
        ('municipal', 'Municipal Corporation'),
        ('ward', 'Ward Committee'),
    ]
    
    name = models.CharField(max_length=200)
    level = models.CharField(max_length=20, choices=LEVELS)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_departments')
    state = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    ward_number = models.CharField(max_length=20, blank=True)
    
    class Meta:
        ordering = ['level', 'name']
        indexes = [
            models.Index(fields=['state', 'district', 'city']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"


class Designation(models.Model):
    """
    Official designations within departments
    """
    title = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='designations')
    level = models.IntegerField(help_text="Escalation ladder position (1=lowest)")
    responsibilities = models.JSONField(default=list, help_text="List of responsibilities")
    typical_response_time = models.IntegerField(null=True, blank=True, help_text="Expected response time in hours")
    
    class Meta:
        ordering = ['department', 'level']
        unique_together = ['department', 'title']
    
    def __str__(self):
        return f"{self.title} - {self.department.name}"


class Officer(models.Model):
    """
    Current officers holding designations
    """
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE, related_name='officers')
    name = models.CharField(max_length=200)
    contact_email = models.EmailField(null=True, blank=True)
    contact_phone = models.CharField(max_length=20, null=True, blank=True)
    office_address = models.TextField(blank=True)
    
    # Crowdsourced verification
    verified_by_users = models.IntegerField(default=0)
    last_verified_at = models.DateTimeField(null=True, blank=True)
    
    # Tenure tracking
    appointed_on = models.DateField(null=True, blank=True)
    tenure_ends_on = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_active', '-verified_by_users']
    
    def __str__(self):
        return f"{self.name} - {self.designation.title}"


class ContactVerification(models.Model):
    """
    User verifications of officer contact details
    """
    officer = models.ForeignKey(Officer, on_delete=models.CASCADE, related_name='verifications')
    verified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    is_correct = models.BooleanField()
    notes = models.TextField(blank=True)
    verified_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-verified_at']
