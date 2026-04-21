from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import PolicyFramework, PolicyRecommendation

class PolicyListView(LoginRequiredMixin, ListView):
    model = PolicyFramework
    template_name = 'policy_guidance/policy_list.html'
    context_object_name = 'policies'
    paginate_by = 15
    
    def get_queryset(self):
        queryset = PolicyFramework.objects.filter(is_active=True).order_by('-created_at')
        
        # Filter by type if provided
        framework_type = self.request.GET.get('type')
        if framework_type:
            queryset = queryset.filter(framework_type=framework_type)
        
        # Filter by region if provided
        region = self.request.GET.get('region')
        if region:
            queryset = queryset.filter(region__icontains=region)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['framework_types'] = PolicyFramework.FRAMEWORK_TYPES
        return context

class PolicyDetailView(LoginRequiredMixin, DetailView):
    model = PolicyFramework
    template_name = 'policy_guidance/policy_detail.html'
    context_object_name = 'policy'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recommendations'] = PolicyRecommendation.objects.filter(
            framework=self.get_object()
        )
        return context

@login_required
def recommendation_detail_view(request, pk):
    recommendation = get_object_or_404(PolicyRecommendation, pk=pk)
    return render(request, 'policy_guidance/recommendation_detail.html', {
        'recommendation': recommendation
    })

@login_required
def sdg_alignment_view(request):
    sdg_policies = PolicyFramework.objects.filter(framework_type='sdg', is_active=True)
    
    context = {
        'sdg_policies': sdg_policies,
    }
    return render(request, 'policy_guidance/sdg_alignment.html', context)
