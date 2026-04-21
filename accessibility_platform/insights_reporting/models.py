from django.db import models
from django.utils import timezone
from user_management.models import CustomUser
from compliance_evaluation.models import AccessibilityProject

class Report(models.Model):
    REPORT_TYPES = (
        ('compliance', 'Compliance Report'),
        ('trend_analysis', 'Trend Analysis'),
        ('user_testing', 'User Testing Report'),
        ('comparison', 'Comparison Report'),
        ('executive_summary', 'Executive Summary'),
    )
    
    FORMATS = (
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('html', 'HTML'),
        ('json', 'JSON'),
    )
    
    project = models.ForeignKey(AccessibilityProject, on_delete=models.CASCADE, related_name='reports')
    generated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    report_format = models.CharField(max_length=20, choices=FORMATS)
    title = models.CharField(max_length=255)
    file_path = models.FileField(upload_to='reports/')
    generated_at = models.DateTimeField(default=timezone.now)
    report_data = models.JSONField(default=dict)
    
    class Meta:
        db_table = 'reports'
        ordering = ['-generated_at']
    
    def __str__(self):
        return f"{self.title} - {self.generated_at}"


class Analytics(models.Model):
    project = models.ForeignKey(AccessibilityProject, on_delete=models.CASCADE, related_name='analytics')
    date = models.DateField(default=timezone.now)
    total_issues_detected = models.IntegerField(default=0)
    issues_resolved = models.IntegerField(default=0)
    compliance_score = models.DecimalField(max_digits=5, decimal_places=2)
    improvement_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    metrics_data = models.JSONField(default=dict)
    
    class Meta:
        db_table = 'analytics'
        ordering = ['-date']
        unique_together = ['project', 'date']
    
    def __str__(self):
        return f"Analytics for {self.project.project_name} on {self.date}"
