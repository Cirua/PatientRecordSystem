from django.contrib import admin
from .models import Patient, Visit, Assessment


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['patient_id', 'full_name', 'date_of_birth', 'gender', 'age', 'registration_date']
    list_filter = ['gender', 'registration_date']
    search_fields = ['patient_id', 'first_name', 'last_name']
    readonly_fields = ['registration_date', 'created_at', 'updated_at', 'age']
    ordering = ['-registration_date']


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ['patient', 'visit_date', 'height', 'weight', 'bmi', 'get_bmi_status']
    list_filter = ['visit_date']
    search_fields = ['patient__patient_id', 'patient__first_name', 'patient__last_name']
    readonly_fields = ['bmi', 'created_at', 'updated_at']
    ordering = ['-visit_date']
    
    def get_bmi_status(self, obj):
        return obj.get_bmi_status()
    get_bmi_status.short_description = 'BMI Status'


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ['visit', 'assessment_type', 'general_health', 'created_at']
    list_filter = ['assessment_type', 'general_health', 'created_at']
    search_fields = ['visit__patient__patient_id', 'visit__patient__first_name', 'visit__patient__last_name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
