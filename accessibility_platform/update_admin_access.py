"""
Script to remove Administrator role from registration and restrict admin panel to superusers only
Run: python update_admin_access.py
"""

import os
import re

# =====================================================
# 1. Update user_management/models.py
# =====================================================
def update_models():
    file_path = 'user_management/models.py'
    
    content = '''from django.contrib.auth.models import AbstractUser
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
'''
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Updated {file_path}")


# =====================================================
# 2. Update user_management/forms.py
# =====================================================
def update_forms():
    file_path = 'user_management/forms.py'
    
    content = '''from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )
    
    role = forms.ChoiceField(
        choices=[
            ('developer', 'Developer'),
            ('designer', 'Designer'),
            ('content_creator', 'Content Creator'),
            ('auditor', 'Auditor'),
            ('accessibility_advocate', 'Accessibility Advocate'),
            ('policymaker', 'Policymaker'),
            ('researcher', 'Researcher'),
            ('analyst', 'Analyst'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    organization_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Organization Name'})
    )
    
    organization_type = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Select Type'),
            ('corporate', 'Corporate'),
            ('government', 'Government'),
            ('non_profit', 'Non-Profit'),
            ('education', 'Education'),
            ('healthcare', 'Healthcare'),
            ('other', 'Other'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role', 'organization_name', 'organization_type']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'organization_name', 
                  'organization_type', 'profile_picture', 'accessibility_goals']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'organization_name': forms.TextInput(attrs={'class': 'form-control'}),
            'organization_type': forms.Select(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'accessibility_goals': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['notification_email', 'notification_in_app', 'report_format', 'theme_preference']
        widgets = {
            'notification_email': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notification_in_app': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'report_format': forms.Select(attrs={'class': 'form-control'}),
            'theme_preference': forms.Select(attrs={'class': 'form-control'}),
        }
'''
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Updated {file_path}")


# =====================================================
# 3. Update admin_management/views.py
# =====================================================
def update_admin_views():
    file_path = 'admin_management/views.py'
    
    content = '''from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Count
from user_management.models import CustomUser
from compliance_evaluation.models import AccessibilityProject
from .models import AccessibilityRule, SystemConfiguration, AuditLog
from .forms import AccessibilityRuleForm, SystemConfigurationForm

# Only superusers can access admin panel
def is_superuser(user):
    return user.is_superuser

# Admin Dashboard
class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'admin_management/admin_dashboard.html'
    context_object_name = 'stats'
    
    def test_func(self):
        return self.request.user.is_superuser
    
    def get_queryset(self):
        return None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_users'] = CustomUser.objects.count()
        context['total_projects'] = AccessibilityProject.objects.count()
        context['active_rules'] = AccessibilityRule.objects.filter(is_active=True).count()
        context['recent_audits'] = AuditLog.objects.all().order_by('-timestamp')[:10]
        context['user_roles'] = CustomUser.objects.values('role').annotate(count=Count('id'))
        return context

# Accessibility Rules List
class RuleListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = AccessibilityRule
    template_name = 'admin_management/rule_list.html'
    context_object_name = 'rules'
    paginate_by = 20
    
    def test_func(self):
        return self.request.user.is_superuser

# Rule Create
class RuleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = AccessibilityRule
    form_class = AccessibilityRuleForm
    template_name = 'admin_management/rule_form.html'
    success_url = reverse_lazy('admin_management:rule_list')
    
    def test_func(self):
        return self.request.user.is_superuser
    
    def form_valid(self, form):
        messages.success(self.request, 'Rule created successfully!')
        return super().form_valid(form)

# Rule Update
class RuleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = AccessibilityRule
    form_class = AccessibilityRuleForm
    template_name = 'admin_management/rule_form.html'
    success_url = reverse_lazy('admin_management:rule_list')
    
    def test_func(self):
        return self.request.user.is_superuser
    
    def form_valid(self, form):
        messages.success(self.request, 'Rule updated successfully!')
        return super().form_valid(form)

# System Configuration
@login_required
@user_passes_test(is_superuser)
def system_configuration_view(request):
    configurations = SystemConfiguration.objects.all().order_by('-updated_at')
    
    if request.method == 'POST':
        config_key = request.POST.get('config_key')
        config_value = request.POST.get('config_value')
        description = request.POST.get('description', '')
        
        config, created = SystemConfiguration.objects.update_or_create(
            config_key=config_key,
            defaults={
                'config_value': config_value,
                'description': description,
                'updated_by': request.user
            }
        )
        
        action = 'created' if created else 'updated'
        messages.success(request, f'Configuration {action} successfully!')
        return redirect('admin_management:system_configuration')
    
    return render(request, 'admin_management/system_configuration.html', {
        'configurations': configurations
    })

# Audit Log
class AuditLogView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = AuditLog
    template_name = 'admin_management/audit_log.html'
    context_object_name = 'logs'
    paginate_by = 50
    ordering = ['-timestamp']
    
    def test_func(self):
        return self.request.user.is_superuser

# User Management
class UserManagementView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CustomUser
    template_name = 'admin_management/user_management.html'
    context_object_name = 'users'
    paginate_by = 20
    
    def test_func(self):
        return self.request.user.is_superuser
'''
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Updated {file_path}")


# =====================================================
# 4. Update templates/base.html (navbar section)
# =====================================================
def update_base_template():
    file_path = 'templates/base.html'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and replace the navbar menu section
        old_pattern = r'{% if user\.role == \'admin\' or user\.is_superuser %}\s*<a href="{% url \'admin_management:admin_dashboard\' %}">Admin Panel</a>\s*{% endif %}'
        new_pattern = '{% if user.is_superuser %}\n                        <a href="{% url \'admin_management:admin_dashboard\' %}">Admin Panel</a>\n                    {% endif %}'
        
        content = re.sub(old_pattern, new_pattern, content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Updated {file_path}")
    except FileNotFoundError:
        print(f"⚠ Warning: {file_path} not found, skipping...")


# =====================================================
# Main execution
# =====================================================
def main():
    print("=" * 60)
    print("UPDATING ADMIN ACCESS RESTRICTIONS")
    print("=" * 60)
    print()
    
    # Update all files
    update_models()
    update_forms()
    update_admin_views()
    update_base_template()
    
    print()
    print("=" * 60)
    print("✓ ALL FILES UPDATED SUCCESSFULLY!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Run: python manage.py makemigrations")
    print("2. Run: python manage.py migrate")
    print("3. Create superuser: python manage.py createsuperuser")
    print("4. Run: python manage.py runserver")
    print()
    print("Changes made:")
    print("- Removed 'Administrator' role from registration")
    print("- Admin panel now accessible only to superusers")
    print("- Updated all forms and views")
    print("- Updated navigation template")
    print()

if __name__ == "__main__":
    main()
