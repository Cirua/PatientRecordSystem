import django_filters
from .models import Patient, Visit


class PatientFilter(django_filters.FilterSet):
    patient_id = django_filters.CharFilter(lookup_expr='icontains')
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    gender = django_filters.ChoiceFilter(choices=Patient.GENDER_CHOICES)
    registration_date = django_filters.DateFilter()
    registration_date_from = django_filters.DateFilter(
        field_name='registration_date',
        lookup_expr='gte'
    )
    registration_date_to = django_filters.DateFilter(
        field_name='registration_date',
        lookup_expr='lte'
    )
    
    class Meta:
        model = Patient
        fields = [
            'patient_id',
            'first_name',
            'last_name',
            'gender',
            'registration_date'
        ]


class VisitFilter(django_filters.FilterSet):
    visit_date = django_filters.DateFilter()
    visit_date_from = django_filters.DateFilter(
        field_name='visit_date',
        lookup_expr='gte'
    )
    visit_date_to = django_filters.DateFilter(
        field_name='visit_date',
        lookup_expr='lte'
    )
    bmi_min = django_filters.NumberFilter(
        field_name='bmi',
        lookup_expr='gte'
    )
    bmi_max = django_filters.NumberFilter(
        field_name='bmi',
        lookup_expr='lte'
    )
    
    class Meta:
        model = Visit
        fields = ['visit_date', 'patient']
