from django.urls import path
from . import views

app_name = 'compliance_evaluation'

urlpatterns = [
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('projects/<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project_update'),
    path('projects/<int:pk>/scan/', views.start_scan_view, name='start_scan'),
    path('issues/<int:pk>/', views.issue_detail_view, name='issue_detail'),
]
