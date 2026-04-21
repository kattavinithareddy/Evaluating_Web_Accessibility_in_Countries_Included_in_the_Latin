from django.urls import path
from . import views

app_name = 'admin_management'

urlpatterns = [
    path('dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('rules/', views.RuleListView.as_view(), name='rule_list'),
    path('rules/create/', views.RuleCreateView.as_view(), name='rule_create'),
    path('rules/<int:pk>/edit/', views.RuleUpdateView.as_view(), name='rule_update'),
    path('configuration/', views.system_configuration_view, name='system_configuration'),
    path('audit-log/', views.AuditLogView.as_view(), name='audit_log'),
    path('users/', views.UserManagementView.as_view(), name='user_management'),
]
