from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Patient, Visit, Assessment
from .serializers import (
    PatientSerializer,
    PatientListSerializer,
    PatientDetailSerializer,
    VisitSerializer,
    AssessmentSerializer
)
from .filters import PatientFilter, VisitFilter


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PatientFilter
    ordering_fields = ['registration_date', 'last_name','middle_name', 'first_name']
    ordering = ['-registration_date']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PatientListSerializer
        elif self.action == 'retrieve':
            return PatientDetailSerializer
        return PatientSerializer
    
    def get_queryset(self):
        queryset = Patient.objects.all()
        
        visit_date = self.request.query_params.get('visit_date', None)
        if visit_date:
            queryset = queryset.filter(visits__visit_date=visit_date).distinct()
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def visits(self, request, pk=None):
        patient = self.get_object()
        visits = patient.visits.all()
        serializer = VisitSerializer(visits, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def check_patient_id(self, request):
        patient_id = request.query_params.get('patient_id', None)
        if not patient_id:
            return Response(
                {'error': 'patient_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        exists = Patient.objects.filter(patient_id=patient_id).exists()
        return Response({'exists': exists})


class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = VisitFilter
    ordering_fields = ['visit_date', 'bmi']
    ordering = ['-visit_date']
    
    def get_queryset(self):
        queryset = Visit.objects.select_related('patient').all()
        
        patient_id = self.request.query_params.get('patient_id', None)
        if patient_id:
            queryset = queryset.filter(patient__patient_id=patient_id)
        
        patient_pk = self.request.query_params.get('patient', None)
        if patient_pk:
            queryset = queryset.filter(patient__id=patient_pk)
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def assessment(self, request, pk=None):
        visit = self.get_object()
        try:
            assessment = visit.assessment
            serializer = AssessmentSerializer(assessment)
            return Response(serializer.data)
        except Assessment.DoesNotExist:
            return Response(
                {'detail': 'No assessment found for this visit.'},
                status=status.HTTP_404_NOT_FOUND
            )


class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Assessment.objects.select_related('visit', 'visit__patient').all()
        
        visit_id = self.request.query_params.get('visit', None)
        if visit_id:
            queryset = queryset.filter(visit__id=visit_id)
        
        assessment_type = self.request.query_params.get('assessment_type', None)
        if assessment_type:
            queryset = queryset.filter(assessment_type=assessment_type)
        
        return queryset
