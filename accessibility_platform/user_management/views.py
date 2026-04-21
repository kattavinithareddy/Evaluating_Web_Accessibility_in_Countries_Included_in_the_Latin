from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, UserProfileForm, UserSettingsForm
from .models import CustomUser

# User Registration
class RegisterView(CreateView):
    template_name = 'user_management/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('user_management:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created successfully! Please log in.')
        return response

# User Login
def login_view(request):
    if request.user.is_authenticated:
        return redirect('user_management:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', 'user_management:dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'user_management/login.html')

# User Logout
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('user_management:login')

# Dashboard
@login_required
def dashboard_view(request):
    try:
        from compliance_evaluation.models import AccessibilityProject, Issue
        
        user = request.user
        
        # Get user's projects
        projects = AccessibilityProject.objects.filter(created_by=user)
        
        # Get statistics
        total_projects = projects.count()
        active_projects = projects.filter(status='scanning').count()
        completed_projects = projects.filter(status='completed').count()
        
        # Get recent issues
        recent_issues = Issue.objects.filter(
            project__created_by=user
        ).order_by('-detected_at')[:5]
        
        # Get critical issues count
        critical_issues = Issue.objects.filter(
            project__created_by=user,
            severity='critical',
            is_resolved=False
        ).count()
        
        context = {
            'total_projects': total_projects,
            'active_projects': active_projects,
            'completed_projects': completed_projects,
            'recent_issues': recent_issues,
            'critical_issues': critical_issues,
            'recent_projects': projects.order_by('-created_at')[:5],
        }
    except Exception as e:
        # Fallback if models don't exist yet
        context = {
            'total_projects': 0,
            'active_projects': 0,
            'completed_projects': 0,
            'recent_issues': [],
            'critical_issues': 0,
            'recent_projects': [],
        }
    
    return render(request, 'user_management/dashboard.html', context)

# User Profile
@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_management:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'user_management/profile.html', {'form': form})

# User Settings
@login_required
def settings_view(request):
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings updated successfully!')
            return redirect('user_management:settings')
    else:
        form = UserSettingsForm(instance=request.user)
    
    return render(request, 'user_management/settings.html', {'form': form})

# User redirect view
def user_redirect_view(request):
    """Redirect /user/ based on authentication status"""
    if request.user.is_authenticated:
        return redirect('user_management:dashboard')
    else:
        return redirect('user_management:login')
