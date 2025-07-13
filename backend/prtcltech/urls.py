"""
URL configuration for prtcltech project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# API Schema documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Bio Research Cursor API",
        default_version='v1',
        description="API for biological research protocol building, data analysis, and visualization",
        terms_of_service="https://www.prtcl.tech/terms/",
        contact=openapi.Contact(email="contact@prtcl.tech"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # API documentation
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API endpoints
    path('api/v1/', include([
        path('protocols/', include('protocols.urls')),
        path('analysis/', include('analysis.urls')),
        path('visualization/', include('visualization.urls')),
        path('users/', include('users.urls')),
    ])),
    
    # Authentication
    path('api/auth/', include('rest_framework.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 