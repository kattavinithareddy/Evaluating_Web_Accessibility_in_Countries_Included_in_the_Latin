from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta
from .models import AccessibilityProject, ComplianceIssue, ScanHistory
from .forms import AccessibilityProjectForm
from ai_engine.utils import run_accessibility_scan
import json

class ProjectListView(LoginRequiredMixin, ListView):
    model = AccessibilityProject
    template_name = 'compliance_evaluation/project_list.html'
    context_object_name = 'projects'
    paginate_by = 10
    
    def get_queryset(self):
        return AccessibilityProject.objects.filter(user=self.request.user).order_by('-created_at')

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = AccessibilityProject
    form_class = AccessibilityProjectForm
    template_name = 'compliance_evaluation/project_create.html'
    success_url = reverse_lazy('compliance_evaluation:project_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Project created successfully!')
        return response

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = AccessibilityProject
    template_name = 'compliance_evaluation/project_detail.html'
    context_object_name = 'project'
    
    def get_queryset(self):
        return AccessibilityProject.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        
        # Get issues grouped by severity
        context['critical_issues'] = ComplianceIssue.objects.filter(
            project=project, severity='critical', is_resolved=False
        )
        context['serious_issues'] = ComplianceIssue.objects.filter(
            project=project, severity='serious', is_resolved=False
        )
        context['moderate_issues'] = ComplianceIssue.objects.filter(
            project=project, severity='moderate', is_resolved=False
        )
        context['minor_issues'] = ComplianceIssue.objects.filter(
            project=project, severity='minor', is_resolved=False
        )
        
        # Get scan history
        context['scan_history'] = ScanHistory.objects.filter(project=project).order_by('-scan_date')[:10]
        
        return context

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = AccessibilityProject
    form_class = AccessibilityProjectForm
    template_name = 'compliance_evaluation/project_update.html'
    
    def get_queryset(self):
        return AccessibilityProject.objects.filter(user=self.request.user)
    
    def get_success_url(self):
        messages.success(self.request, 'Project updated successfully!')
        return reverse_lazy('compliance_evaluation:project_detail', kwargs={'pk': self.object.pk})

@login_required
def start_scan_view(request, pk):
    project = get_object_or_404(AccessibilityProject, pk=pk, user=request.user)
    
    if project.status == 'scanning':
        messages.warning(request, 'Scan is already in progress for this project.')
        return redirect('compliance_evaluation:project_detail', pk=pk)
    
    # Update project status
    project.status = 'scanning'
    project.save()
    
    # Run accessibility scan (async in production)
    try:
        scan_results = run_accessibility_scan(project)
        messages.success(request, 'Scan completed successfully!')
    except Exception as e:
        project.status = 'failed'
        project.save()
        messages.error(request, f'Scan failed: {str(e)}')
    
    return redirect('compliance_evaluation:project_detail', pk=pk)

@login_required
def issue_detail_view(request, pk):
    issue = get_object_or_404(ComplianceIssue, pk=pk, project__user=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'resolve':
            issue.is_resolved = True
            issue.resolved_at = timezone.now()
            issue.save()
            messages.success(request, 'Issue marked as resolved!')
        elif action == 'unresolve':
            issue.is_resolved = False
            issue.resolved_at = None
            issue.save()
            messages.success(request, 'Issue marked as unresolved!')
        
        return redirect('compliance_evaluation:issue_detail', pk=pk)
    
    return render(request, 'compliance_evaluation/issue_detail.html', {'issue': issue})
