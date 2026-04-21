from django.db import models
from django.utils import timezone
from user_management.models import CustomUser

class AccessibilityRule(models.Model):
    WCAG_LEVELS = (
        ('A', 'Level A'),
        ('AA', 'Level AA'),
        ('AAA', 'Level AAA'),
    )
    
    rule_id = models.CharField(max_length=50, unique=True)
    wcag_criterion = models.CharField(max_length=50)
    wcag_level = models.CharField(max_length=5, choices=WCAG_LEVELS)
    rule_name = models.CharField(max_length=255)
    description = models.TextField()
    testing_procedure = models.TextField()
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)
    severity_default = models.CharField(max_length=20, choices=[('critical', 'Critical'), ('serious', 'Serious'), ('moderate', 'Moderate'), ('minor', 'Minor')])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'accessibility_rules'
    
    def __str__(self):
        return f"{self.rule_id} - {self.rule_name}"


class SystemConfiguration(models.Model):
    config_key = models.CharField(max_length=100, unique=True)
    config_value = models.TextField()
    description = models.TextField(blank=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'system_configurations'
    
    def __str__(self):
        return self.config_key


class AuditLog(models.Model):
    ACTION_TYPES = (
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('scan', 'Scan'),
        ('export', 'Export'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    action_type = models.CharField(max_length=50, choices=ACTION_TYPES)
    model_name = models.CharField(max_length=100)
    object_id = models.IntegerField(null=True, blank=True)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'audit_logs'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.action_type} by {self.user} at {self.timestamp}"
