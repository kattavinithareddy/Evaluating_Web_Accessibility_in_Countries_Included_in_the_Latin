from django.urls import path
from . import views

app_name = 'user_testing'

urlpatterns = [
    path('programs/', views.TestingProgramListView.as_view(), name='program_list'),
    path('programs/create/', views.TestingProgramCreateView.as_view(), name='program_create'),
    path('programs/<int:pk>/', views.TestingProgramDetailView.as_view(), name='program_detail'),
    path('tester/register/', views.tester_registration_view, name='tester_registration'),
    path('tester/dashboard/', views.tester_dashboard_view, name='tester_dashboard'),
    path('tasks/<int:pk>/', views.task_detail_view, name='task_detail'),
    path('tasks/<int:task_id>/feedback/', views.submit_feedback_view, name='submit_feedback'),
]
