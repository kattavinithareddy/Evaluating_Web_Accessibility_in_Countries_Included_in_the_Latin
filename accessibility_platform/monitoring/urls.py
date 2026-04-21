from django.urls import path
from . import views

app_name = 'monitoring'

urlpatterns = [
    path('dashboard/', views.monitoring_dashboard_view, name='monitoring_dashboard'),
    path('notifications/', views.NotificationListView.as_view(), name='notification_list'),
    path('notifications/<int:pk>/read/', views.mark_notification_read_view, name='mark_read'),
    path('notifications/mark-all-read/', views.mark_all_read_view, name='mark_all_read'),
    path('schedule/create/<int:project_id>/', views.create_schedule_view, name='create_schedule'),
    path('schedule/<int:pk>/toggle/', views.toggle_schedule_view, name='toggle_schedule'),
    path('alert-rules/', views.alert_rules_view, name='alert_rules'),
    path('alert-rules/create/<int:project_id>/', views.create_alert_rule_view, name='create_alert_rule'),
]
