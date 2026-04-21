from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, FileResponse
from django.utils import timezone
from datetime import timedelta, datetime
import json
from .models import Report, Analytics
from .forms import ReportGenerationForm
from compliance_evaluation.models import AccessibilityProject, ComplianceIssue, ScanHistory
from .utils import generate_pdf_report, generate_excel_report, generate_html_report

@login_required
def reports_list_view(request):
    projects = AccessibilityProject.objects.filter(user=request.user)
    reports = Report.objects.filter(project__user=request.user).order_by('-generated_at')[:20]
    
    context = {
        'projects': projects,
        'reports': reports,
    }
    return render(request, 'insights_reporting/reports_list.html', context)

@login_required
def generate_report_view(request, project_id):
    project = get_object_or_404(AccessibilityProject, pk=project_id, user=request.user)
    
    if request.method == 'POST':
        form = ReportGenerationForm(request.POST)
        if form.is_valid():
            report_type = form.cleaned_data['report_type']
            report_format = form.cleaned_data['report_format']
            
            # Prepare report data
            issues = ComplianceIssue.objects.filter(project=project)
            scan_history = ScanHistory.objects.filter(project=project).order_by('-scan_date')[:10]
            
            report_data = {
                'project': {
                    'name': project.project_name,
                    'url': project.url,
                    'compliance_score': float(project.compliance_score) if project.compliance_score else 0,
                    'wcag_level': project.wcag_level_target,
                },
                'issues': {
                    'critical': issues.filter(severity='critical', is_resolved=False).count(),
                    'serious': issues.filter(severity='serious', is_resolved=False).count(),
                    'moderate': issues.filter(severity='moderate', is_resolved=False).count(),
                    'minor': issues.filter(severity='minor', is_resolved=False).count(),
                },
                'total_issues': issues.count(),
                'resolved_issues': issues.filter(is_resolved=True).count(),
            }
            
            # Generate report based on format
            if report_format == 'pdf':
                file_path = generate_pdf_report(project, report_data, report_type)
            elif report_format == 'excel':
                file_path = generate_excel_report(project, report_data, report_type)
            else:
                file_path = generate_html_report(project, report_data, report_type)
            
            # Save report to database
            report = Report.objects.create(
                project=project,
                generated_by=request.user,
                report_type=report_type,
                report_format=report_format,
                title=f"{report_type.replace('_', ' ').title()} - {project.project_name}",
                file_path=file_path,
                report_data=report_data
            )
            
            messages.success(request, 'Report generated successfully!')
            return redirect('insights_reporting:report_detail', pk=report.pk)
    else:
        form = ReportGenerationForm()
    
    return render(request, 'insights_reporting/generate_report.html', {'form': form, 'project': project})

class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = 'insights_reporting/report_detail.html'
    context_object_name = 'report'
    
    def get_queryset(self):
        return Report.objects.filter(project__user=self.request.user)

@login_required
def download_report_view(request, pk):
    report = get_object_or_404(Report, pk=pk, project__user=request.user)
    
    try:
        response = FileResponse(open(report.file_path.path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{report.title}.{report.report_format}"'
        return response
    except FileNotFoundError:
        messages.error(request, 'Report file not found.')
        return redirect('insights_reporting:reports_list')

@login_required
def analytics_dashboard_view(request):
    projects = AccessibilityProject.objects.filter(user=request.user)
    
    # Get date range for analytics
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    # Prepare analytics data
    analytics_data = []
    for project in projects:
        recent_analytics = Analytics.objects.filter(
            project=project,
            date__range=[start_date, end_date]
        ).order_by('date')
        
        if recent_analytics.exists():
            analytics_data.append({
                'project': project,
                'data': recent_analytics
            })
    
    # Calculate overall statistics
    total_issues = ComplianceIssue.objects.filter(project__user=request.user).count()
    resolved_issues = ComplianceIssue.objects.filter(project__user=request.user, is_resolved=True).count()
    avg_compliance = 0
    
    projects_with_scores = projects.filter(compliance_score__isnull=False)
    if projects_with_scores.exists():
        total_score = sum([float(p.compliance_score) for p in projects_with_scores])
        avg_compliance = total_score / projects_with_scores.count()
    
    context = {
        'projects': projects,
        'analytics_data': analytics_data,
        'total_issues': total_issues,
        'resolved_issues': resolved_issues,
        'avg_compliance': round(avg_compliance, 2),
    }
    return render(request, 'insights_reporting/analytics_dashboard.html', context)
