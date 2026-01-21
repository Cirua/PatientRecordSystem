from rest_framework import serializers
from .models import Patient, Visit, Assessment
from datetime import date
from decimal import Decimal


class PatientSerializer(serializers.ModelSerializer):
    age = serializers.ReadOnlyField()
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Patient
        fields = [
            'id',
            'patient_id',
            'first_name',
            'last_name',
            'full_name',
            'date_of_birth',
            'gender',
            'age',
            'registration_date',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'registration_date', 'created_at', 'updated_at']
    
    def validate_patient_id(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Patient ID cannot be empty.")
        
        if self.instance is None:
            if Patient.objects.filter(patient_id=value).exists():
                raise serializers.ValidationError(
                    "A patient with this Patient ID already exists."
                )
        
        return value.strip()
    
    def validate_date_of_birth(self, value):
        if value > date.today():
            raise serializers.ValidationError(
                "Date of birth cannot be in the future."
            )
        
        age = date.today().year - value.year
        if age > 150:
            raise serializers.ValidationError(
                "Invalid date of birth. Age cannot exceed 150 years."
            )
        
        return value


class VisitSerializer(serializers.ModelSerializer):
    bmi_status = serializers.SerializerMethodField()
    patient_id = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Visit
        fields = [
            'id',
            'patient',
            'patient_id',
            'visit_date',
            'height',
            'weight',
            'bmi',
            'bmi_status',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'bmi', 'created_at', 'updated_at']
    
    def get_bmi_status(self, obj):
        return obj.get_bmi_status()
    
    def validate_visit_date(self, value):
        if value > date.today():
            raise serializers.ValidationError(
                "Visit date cannot be in the future."
            )
        return value
    
    def validate_height(self, value):
        if value < Decimal('30.0') or value > Decimal('300.0'):
            raise serializers.ValidationError(
                "Height must be between 30 and 300 cm."
            )
        return value
    
    def validate_weight(self, value):
        if value < Decimal('1.0') or value > Decimal('500.0'):
            raise serializers.ValidationError(
                "Weight must be between 1 and 500 kg."
            )
        return value
    
    def validate(self, data):
        patient = data.get('patient')
        visit_date = data.get('visit_date')
        
        if patient and visit_date:
            if self.instance is None:
                if Visit.objects.filter(patient=patient, visit_date=visit_date).exists():
                    raise serializers.ValidationError(
                        "A visit for this patient on this date already exists."
                    )
        
        return data
    
    def create(self, validated_data):
        validated_data.pop('patient_id', None)
        return super().create(validated_data)


class AssessmentSerializer(serializers.ModelSerializer):
    visit_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Assessment
        fields = [
            'id',
            'visit',
            'visit_id',
            'assessment_type',
            'general_health',
            'on_diet',
            'using_drugs',
            'comments',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, data):
        assessment_type = data.get('assessment_type')
        on_diet = data.get('on_diet')
        using_drugs = data.get('using_drugs')
        
        if assessment_type == 'overweight':
            if on_diet is None:
                raise serializers.ValidationError({
                    'on_diet': 'This field is required for overweight assessments.'
                })
            if using_drugs is not None:
                raise serializers.ValidationError({
                    'using_drugs': 'This field should not be provided for overweight assessments.'
                })
        elif assessment_type == 'general':
            if using_drugs is None:
                raise serializers.ValidationError({
                    'using_drugs': 'This field is required for general assessments.'
                })
            if on_diet is not None:
                raise serializers.ValidationError({
                    'on_diet': 'This field should not be provided for general assessments.'
                })
        
        visit = data.get('visit')
        if visit:
            if assessment_type == 'overweight' and not visit.requires_overweight_assessment():
                raise serializers.ValidationError(
                    "Overweight assessment is only for patients with BMI > 25."
                )
            elif assessment_type == 'general' and visit.requires_overweight_assessment():
                raise serializers.ValidationError(
                    "General assessment is only for patients with BMI ≤ 25."
                )
        
        return data
    
    def create(self, validated_data):
        visit_id = validated_data.pop('visit_id', None)
        if visit_id:
            try:
                validated_data['visit'] = Visit.objects.get(id=visit_id)
            except Visit.DoesNotExist:
                raise serializers.ValidationError({'visit_id': 'Visit not found.'})
        
        return super().create(validated_data)


class PatientListSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    age = serializers.ReadOnlyField()
    last_bmi_status = serializers.SerializerMethodField()
    last_assessment_date = serializers.SerializerMethodField()
    
    class Meta:
        model = Patient
        fields = [
            'id',
            'patient_id',
            'patient_name',
            'age',
            'last_bmi_status',
            'last_assessment_date'
        ]
    
    def get_patient_name(self, obj):
        return obj.full_name
    
    def get_last_bmi_status(self, obj):
        return obj.get_latest_bmi_status()
    
    def get_last_assessment_date(self, obj):
        date_obj = obj.get_latest_assessment_date()
        if date_obj:
            return date_obj.strftime('%Y-%m-%d')
        return None


class PatientDetailSerializer(serializers.ModelSerializer):
    age = serializers.ReadOnlyField()
    full_name = serializers.ReadOnlyField()
    visits = VisitSerializer(many=True, read_only=True)
    
    class Meta:
        model = Patient
        fields = [
            'id',
            'patient_id',
            'first_name',
            'last_name',
            'full_name',
            'date_of_birth',
            'gender',
            'age',
            'registration_date',
            'visits',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'registration_date', 'created_at', 'updated_at']
