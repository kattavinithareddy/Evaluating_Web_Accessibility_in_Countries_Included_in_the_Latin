from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('developer', 'Developer'),
        ('designer', 'Designer'),
        ('content_creator', 'Content Creator'),
        ('auditor', 'Auditor'),
        ('accessibility_advocate', 'Accessibility Advocate'),
        ('policymaker', 'Policymaker'),
        ('researcher', 'Researcher'),
        ('analyst', 'Analyst'),
    ]
    
    ORGANIZATION_TYPE_CHOICES = [
        ('corporate', 'Corporate'),
        ('government', 'Government'),
        ('non_profit', 'Non-Profit'),
        ('education', 'Education'),
        ('healthcare', 'Healthcare'),
        ('other', 'Other'),
    ]
    
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='developer')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    organization_name = models.CharField(max_length=255, blank=True, null=True)
    organization_type = models.CharField(max_length=50, choices=ORGANIZATION_TYPE_CHOICES, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    accessibility_goals = models.TextField(blank=True, null=True)
    
    # Preferences
    notification_email = models.BooleanField(default=True)
    notification_in_app = models.BooleanField(default=True)
    report_format = models.CharField(max_length=10, default='pdf', choices=[('pdf', 'PDF'), ('excel', 'Excel'), ('html', 'HTML')])
    theme_preference = models.CharField(max_length=10, default='light', choices=[('light', 'Light'), ('dark', 'Dark')])
    
    def __str__(self):
        return self.username
