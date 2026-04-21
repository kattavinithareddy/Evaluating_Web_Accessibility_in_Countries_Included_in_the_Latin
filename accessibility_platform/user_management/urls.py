from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'user_management'

urlpatterns = [
    # Redirect /user/ to /user/login/
    path('', RedirectView.as_view(pattern_name='user_management:login', permanent=False), name='user_redirect'),
    
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('settings/', views.settings_view, name='settings'),
]
