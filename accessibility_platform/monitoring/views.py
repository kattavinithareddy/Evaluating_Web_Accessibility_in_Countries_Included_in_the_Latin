from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import timedelta
from .models import MonitoringSchedule, Notification, AlertRule
from .forms import MonitoringScheduleForm, AlertRuleForm
from compliance_evaluation.models import AccessibilityProject

@login_required
def monitoring_dashboard_view(request):
    active_schedules = MonitoringSchedule.objects.filter(
        project__user=request.user,
        is_active=True
    )
    recent_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:10]
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    
    context = {
        'active_schedules': active_schedules,
        'recent_notifications': recent_notifications,
        'unread_count': unread_count,
    }
    return render(request, 'monitoring/monitoring_dashboard.html', context)

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'monitoring/notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 20
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

@login_required
def mark_notification_read_view(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.read_at = timezone.now()
    notification.save()
    return redirect('monitoring:notification_list')

@login_required
def mark_all_read_view(request):
    Notification.objects.filter(user=request.user, is_read=False).update(
        is_read=True,
        read_at=timezone.now()
    )
    messages.success(request, 'All notifications marked as read.')
    return redirect('monitoring:notification_list')

@login_required
def create_schedule_view(request, project_id):
    project = get_object_or_404(AccessibilityProject, pk=project_id, user=request.user)
    
    if request.method == 'POST':
        form = MonitoringScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.project = project
            
            # Calculate next scan date based on frequency
            if schedule.frequency == 'daily':
                schedule.next_scan_date = timezone.now() + timedelta(days=1)
            elif schedule.frequency == 'weekly':
                schedule.next_scan_date = timezone.now() + timedelta(weeks=1)
            elif schedule.frequency == 'biweekly':
                schedule.next_scan_date = timezone.now() + timedelta(weeks=2)
            else:  # monthly
                schedule.next_scan_date = timezone.now() + timedelta(days=30)
            
            schedule.save()
            messages.success(request, 'Monitoring schedule created successfully!')
            return redirect('monitoring:monitoring_dashboard')
    else:
        form = MonitoringScheduleForm()
    
    return render(request, 'monitoring/create_schedule.html', {'form': form, 'project': project})

@login_required
def toggle_schedule_view(request, pk):
    schedule = get_object_or_404(MonitoringSchedule, pk=pk, project__user=request.user)
    schedule.is_active = not schedule.is_active
    schedule.save()
    
    status = 'activated' if schedule.is_active else 'deactivated'
    messages.success(request, f'Monitoring schedule {status}.')
    return redirect('monitoring:monitoring_dashboard')

@login_required
def alert_rules_view(request):
    projects = AccessibilityProject.objects.filter(user=request.user)
    rules = AlertRule.objects.filter(project__user=request.user)
    
    context = {
        'projects': projects,
        'rules': rules,
    }
    return render(request, 'monitoring/alert_rules.html', context)

@login_required
def create_alert_rule_view(request, project_id):
    project = get_object_or_404(AccessibilityProject, pk=project_id, user=request.user)
    
    if request.method == 'POST':
        form = AlertRuleForm(request.POST)
        if form.is_valid():
            rule = form.save(commit=False)
            rule.project = project
            rule.save()
            messages.success(request, 'Alert rule created successfully!')
            return redirect('monitoring:alert_rules')
    else:
        form = AlertRuleForm()
    
    return render(request, 'monitoring/create_alert_rule.html', {'form': form, 'project': project})
