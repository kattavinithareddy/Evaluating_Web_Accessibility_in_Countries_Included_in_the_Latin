from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Redirect root to login page
    path('', RedirectView.as_view(url='/user/login/', permanent=False)),
    
    # User-facing modules
    path('user/', include('user_management.urls')),
    path('compliance/', include('compliance_evaluation.urls')),
    path('testing/', include('user_testing.urls')),
    path('insights/', include('insights_reporting.urls')),
    path('monitoring/', include('monitoring.urls')),
    path('policy/', include('policy_guidance.urls')),
    
    # Admin modules
    path('admin-panel/', include('admin_management.urls')),
    path('ai-engine/', include('ai_engine.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "Accessibility Platform Admin"
admin.site.site_title = "Accessibility Platform"
admin.site.index_title = "Welcome to Accessibility Platform Administration"
