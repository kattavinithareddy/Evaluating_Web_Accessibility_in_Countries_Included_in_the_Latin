from django.urls import path
from . import views

app_name = 'policy_guidance'

urlpatterns = [
    path('policies/', views.PolicyListView.as_view(), name='policy_list'),
    path('policies/<int:pk>/', views.PolicyDetailView.as_view(), name='policy_detail'),
    path('recommendations/<int:pk>/', views.recommendation_detail_view, name='recommendation_detail'),
    path('sdg-alignment/', views.sdg_alignment_view, name='sdg_alignment'),
]
