from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'files', views.DataFileViewSet, basename='datafile')
router.register(r'tasks', views.AnalysisTaskViewSet, basename='analysistask')
router.register(r'templates', views.AnalysisTemplateViewSet, basename='analysistemplate')

urlpatterns = [
    path('', include(router.urls)),
] 