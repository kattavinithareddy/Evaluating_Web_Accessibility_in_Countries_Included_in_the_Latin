from django.db import models
from django.utils import timezone

class PolicyFramework(models.Model):
    FRAMEWORK_TYPES = (
        ('national', 'National Law'),
        ('international', 'International Standard'),
        ('institutional', 'Institutional Policy'),
        ('sdg', 'SDG Alignment'),
        ('wcag', 'WCAG Guideline'),
    )
    
    framework_name = models.CharField(max_length=255)
    framework_type = models.CharField(max_length=50, choices=FRAMEWORK_TYPES)
    description = models.TextField()
    region = models.CharField(max_length=100, blank=True, null=True)
    effective_date = models.DateField(null=True, blank=True)
    reference_url = models.URLField(max_length=500, blank=True, null=True)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'policy_frameworks'
    
    def __str__(self):
        return f"{self.framework_name} ({self.framework_type})"


class PolicyRecommendation(models.Model):
    framework = models.ForeignKey(PolicyFramework, on_delete=models.CASCADE, related_name='recommendations')
    recommendation_title = models.CharField(max_length=255)
    description = models.TextField()
    target_audience = models.CharField(max_length=255)
    implementation_steps = models.TextField()
    priority_level = models.CharField(max_length=20, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'policy_recommendations'
    
    def __str__(self):
        return self.recommendation_title
