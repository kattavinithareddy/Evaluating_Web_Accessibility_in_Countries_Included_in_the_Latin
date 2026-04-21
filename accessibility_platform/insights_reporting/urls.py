from django.urls import path
from . import views

app_name = 'insights_reporting'

urlpatterns = [
    path('reports/', views.reports_list_view, name='reports_list'),
    path('reports/generate/<int:project_id>/', views.generate_report_view, name='generate_report'),
    path('reports/<int:pk>/', views.ReportDetailView.as_view(), name='report_detail'),
    path('reports/<int:pk>/download/', views.download_report_view, name='download_report'),
    path('analytics/', views.analytics_dashboard_view, name='analytics_dashboard'),
]
