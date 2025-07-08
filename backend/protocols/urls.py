from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_nested import routers
from . import views

# Create the main router
router = DefaultRouter()
router.register(r'protocols', views.ProtocolViewSet, basename='protocol')
router.register(r'papers', views.ResearchPaperViewSet, basename='paper')

# Create nested routers for protocol-related resources
protocol_router = routers.NestedDefaultRouter(router, r'protocols', lookup='protocol')
protocol_router.register(r'steps', views.ProtocolStepViewSet, basename='protocol-step')
protocol_router.register(r'reagents', views.ReagentViewSet, basename='protocol-reagent')
protocol_router.register(r'references', views.ProtocolReferenceViewSet, basename='protocol-reference')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(protocol_router.urls)),
] 