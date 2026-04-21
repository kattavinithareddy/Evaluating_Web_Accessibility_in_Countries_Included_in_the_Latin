from django.shortcuts import render, redirect, get_object_or_404
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
