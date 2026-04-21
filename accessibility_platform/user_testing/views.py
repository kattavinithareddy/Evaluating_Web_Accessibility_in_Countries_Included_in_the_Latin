from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from .models import UserTestingProgram, Tester, TestTask, UserFeedback
from .forms import UserTestingProgramForm, TesterForm, TestTaskForm, UserFeedbackForm
from compliance_evaluation.models import AccessibilityProject

class TestingProgramListView(LoginRequiredMixin, ListView):
    model = UserTestingProgram
    template_name = 'user_testing/program_list.html'
    context_object_name = 'programs'
    paginate_by = 10
    
    def get_queryset(self):
        return UserTestingProgram.objects.filter(
            coordinator=self.request.user
        ).order_by('-created_at')

class TestingProgramCreateView(LoginRequiredMixin, CreateView):
    model = UserTestingProgram
    form_class = UserTestingProgramForm
    template_name = 'user_testing/program_create.html'
    success_url = reverse_lazy('user_testing:program_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.coordinator = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Testing program created successfully!')
        return response

class TestingProgramDetailView(LoginRequiredMixin, DetailView):
    model = UserTestingProgram
    template_name = 'user_testing/program_detail.html'
    context_object_name = 'program'
    
    def get_queryset(self):
        return UserTestingProgram.objects.filter(coordinator=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        program = self.get_object()
        context['tasks'] = TestTask.objects.filter(program=program)
        context['completed_tasks'] = TestTask.objects.filter(program=program, status='completed').count()
        return context

@login_required
def tester_registration_view(request):
    try:
        tester = request.user.tester_profile
        messages.info(request, 'You are already registered as a tester.')
        return redirect('user_testing:tester_dashboard')
    except Tester.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = TesterForm(request.POST)
        if form.is_valid():
            tester = form.save(commit=False)
            tester.user = request.user
            tester.consent_date = timezone.now()
            tester.save()
            messages.success(request, 'Tester registration successful!')
            return redirect('user_testing:tester_dashboard')
    else:
        form = TesterForm()
    
    return render(request, 'user_testing/tester_registration.html', {'form': form})

@login_required
def tester_dashboard_view(request):
    try:
        tester = request.user.tester_profile
    except Tester.DoesNotExist:
        messages.warning(request, 'Please register as a tester first.')
        return redirect('user_testing:tester_registration')
    
    pending_tasks = TestTask.objects.filter(tester=tester, status='pending')
    in_progress_tasks = TestTask.objects.filter(tester=tester, status='in_progress')
    completed_tasks = TestTask.objects.filter(tester=tester, status='completed')
    
    context = {
        'tester': tester,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completed_tasks': completed_tasks,
    }
    return render(request, 'user_testing/tester_dashboard.html', context)

@login_required
def task_detail_view(request, pk):
    task = get_object_or_404(TestTask, pk=pk, tester__user=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'start':
            task.status = 'in_progress'
            task.save()
            messages.success(request, 'Task started!')
        elif action == 'complete':
            task.status = 'completed'
            task.completed_at = timezone.now()
            task.save()
            messages.success(request, 'Task completed!')
        
        return redirect('user_testing:task_detail', pk=pk)
    
    feedback = UserFeedback.objects.filter(task=task).first()
    return render(request, 'user_testing/task_detail.html', {'task': task, 'feedback': feedback})

@login_required
def submit_feedback_view(request, task_id):
    task = get_object_or_404(TestTask, pk=task_id, tester__user=request.user)
    
    if request.method == 'POST':
        form = UserFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.task = task
            feedback.save()
            
            # Mark task as completed
            task.status = 'completed'
            task.completed_at = timezone.now()
            task.save()
            
            messages.success(request, 'Feedback submitted successfully!')
            return redirect('user_testing:tester_dashboard')
    else:
        form = UserFeedbackForm()
    
    return render(request, 'user_testing/submit_feedback.html', {'form': form, 'task': task})
