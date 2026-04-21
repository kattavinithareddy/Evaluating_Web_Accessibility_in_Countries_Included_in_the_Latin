from django.db import models
from django.utils import timezone
from user_management.models import CustomUser
from compliance_evaluation.models import AccessibilityProject

class MonitoringSchedule(models.Model):
    FREQUENCY_CHOICES = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('biweekly', 'Bi-Weekly'),
        ('monthly', 'Monthly'),
    )
    
    project = models.ForeignKey(AccessibilityProject, on_delete=models.CASCADE, related_name='monitoring_schedules')
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    is_active = models.BooleanField(default=True)
    next_scan_date = models.DateTimeField()
    last_scan_date = models.DateTimeField(null=True, blank=True)
    notification_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'monitoring_schedules'
    
    def __str__(self):
        return f"Monitor {self.project.project_name} - {self.frequency}"


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('new_issue', 'New Issue Detected'),
        ('regression', 'Regression Detected'),
        ('improvement', 'Improvement Detected'),
        ('scan_complete', 'Scan Complete'),
        ('scan_failed', 'Scan Failed'),
        ('reminder', 'Reminder'),
    )
    
    PRIORITY_LEVELS = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    project = models.ForeignKey(AccessibilityProject, on_delete=models.CASCADE, null=True, blank=True)
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    priority = models.CharField(max_length=20, choices=PRIORITY_LEVELS, default='medium')
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"


class AlertRule(models.Model):
    project = models.ForeignKey(AccessibilityProject, on_delete=models.CASCADE, related_name='alert_rules')
    rule_name = models.CharField(max_length=255)
    condition = models.JSONField(help_text="JSON structure defining alert conditions")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'alert_rules'
    
    def __str__(self):
        return f"{self.rule_name} - {self.project.project_name}"
