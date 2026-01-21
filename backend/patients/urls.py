from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, VisitViewSet, AssessmentViewSet

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'visits', VisitViewSet, basename='visit')
router.register(r'assessments', AssessmentViewSet, basename='assessment')

urlpatterns = [
    path('', include(router.urls)),
]
