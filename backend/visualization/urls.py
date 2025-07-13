from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'visualizations', views.VisualizationViewSet, basename='visualization')
router.register(r'chart-data', views.ChartDataViewSet, basename='chartdata')
router.register(r'templates', views.ChartTemplateViewSet, basename='charttemplate')

urlpatterns = [
    path('', include(router.urls)),
] 