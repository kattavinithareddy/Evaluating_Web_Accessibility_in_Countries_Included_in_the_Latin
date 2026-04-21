from django.db import models
from django.utils import timezone
from user_management.models import CustomUser

class AccessibilityProject(models.Model):
    PROJECT_TYPES = (
        ('website', 'Website'),
        ('mobile_app', 'Mobile Application'),
        ('web_app', 'Web Application'),
        ('desktop_app', 'Desktop Application'),
        ('document', 'Document/PDF'),
    )
    
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('scanning', 'Scanning'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='projects')
    project_name = models.CharField(max_length=255)
    project_type = models.CharField(max_length=50, choices=PROJECT_TYPES)
    url = models.URLField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='draft')
    compliance_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    wcag_level_target = models.CharField(max_length=10, choices=[('A', 'Level A'), ('AA', 'Level AA'), ('AAA', 'Level AAA')], default='AA')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    last_scanned = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'accessibility_projects'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.project_name} - {self.user.username}"


class ComplianceIssue(models.Model):
    SEVERITY_LEVELS = (
        ('critical', 'Critical'),
        ('serious', 'Serious'),
        ('moderate', 'Moderate'),
        ('minor', 'Minor'),
    )
    
    ISSUE_CATEGORIES = (
        ('alt_text', 'Missing Alt Text'),
        ('color_contrast', 'Color Contrast'),
        ('keyboard_navigation', 'Keyboard Navigation'),
        ('form_labels', 'Form Labels'),
        ('heading_structure', 'Heading Structure'),
        ('aria_attributes', 'ARIA Attributes'),
        ('language', 'Language Declaration'),
        ('focus_indicators', 'Focus Indicators'),
        ('text_resize', 'Text Resize'),
        ('link_text', 'Link Text'),
        ('other', 'Other'),
    )
    
    project = models.ForeignKey(AccessibilityProject, on_delete=models.CASCADE, related_name='issues')
    issue_type = models.CharField(max_length=100, choices=ISSUE_CATEGORIES)
    severity = models.CharField(max_length=50, choices=SEVERITY_LEVELS)
    wcag_criterion = models.CharField(max_length=50)  # e.g., "1.1.1", "1.4.3"
    description = models.TextField()
    element_selector = models.CharField(max_length=500, blank=True, null=True)
    page_url = models.URLField(max_length=500)
    code_snippet = models.TextField(blank=True, null=True)
    recommendation = models.TextField()
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    detected_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'compliance_issues'
        ordering = ['-detected_at']
    
    def __str__(self):
        return f"{self.issue_type} - {self.severity} ({self.project.project_name})"


class ScanHistory(models.Model):
    project = models.ForeignKey(AccessibilityProject, on_delete=models.CASCADE, related_name='scan_history')
    scan_date = models.DateTimeField(default=timezone.now)
    compliance_score = models.DecimalField(max_digits=5, decimal_places=2)
    total_issues = models.IntegerField(default=0)
    critical_issues = models.IntegerField(default=0)
    serious_issues = models.IntegerField(default=0)
    moderate_issues = models.IntegerField(default=0)
    minor_issues = models.IntegerField(default=0)
    scan_duration = models.DurationField(null=True, blank=True)
    scan_details = models.JSONField(default=dict)
    
    class Meta:
        db_table = 'scan_history'
        ordering = ['-scan_date']
    
    def __str__(self):
        return f"Scan for {self.project.project_name} on {self.scan_date}"
