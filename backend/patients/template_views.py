from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from datetime import date
from decimal import Decimal
from .models import Patient, Visit, Assessment


@require_http_methods(["GET", "POST"])
def patient_registration(request):
    """Handle patient registration form"""
    context = {
        'today': date.today().isoformat(),
        'form_data': {},
        'error': None,
        'success': None
    }
    
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        middle_name = request.POST.get('middle_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        
        context['form_data'] = {
            'patient_id': patient_id,
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'date_of_birth': date_of_birth,
            'gender': gender
        }
        
        if not all([patient_id, first_name, last_name, date_of_birth, gender]):
            context['error'] = 'All fields are required.'
            return render(request, 'patient_registration.html', context)
        
        if Patient.objects.filter(patient_id=patient_id).exists():
            context['error'] = 'A patient with this Patient ID already exists. Please use a different ID.'
            return render(request, 'patient_registration.html', context)
        
        try:
            patient = Patient.objects.create(
                patient_id=patient_id,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                date_of_birth=date_of_birth,
                gender=gender
            )
            return redirect('vitals_form', patient_id=patient.patient_id)
        except Exception as e:
            context['error'] = f'Error creating patient: {str(e)}'
            return render(request, 'patient_registration.html', context)
    
    return render(request, 'patient_registration.html', context)


@require_http_methods(["GET", "POST"])
def vitals_form(request, patient_id):
    """Handle vitals form submission"""
    patient = get_object_or_404(Patient, patient_id=patient_id)
    
    context = {
        'patient': patient,
        'today': date.today().isoformat(),
        'form_data': {},
        'error': None,
        'bmi': None,
        'bmi_status': None,
        'bmi_status_class': None
    }
    
    if request.method == 'POST':
        visit_date = request.POST.get('visit_date')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        
        context['form_data'] = {
            'visit_date': visit_date,
            'height': height,
            'weight': weight
        }
        
        if not all([visit_date, height, weight]):
            context['error'] = 'All fields are required.'
            return render(request, 'vitals_form.html', context)
        
        try:
            height_decimal = Decimal(height)
            weight_decimal = Decimal(weight)
            
            if height_decimal < 30 or height_decimal > 300:
                context['error'] = 'Height must be between 30 and 300 cm.'
                return render(request, 'vitals_form.html', context)
            
            if weight_decimal < 1 or weight_decimal > 500:
                context['error'] = 'Weight must be between 1 and 500 kg.'
                return render(request, 'vitals_form.html', context)
            
            if Visit.objects.filter(patient=patient, visit_date=visit_date).exists():
                context['error'] = 'A visit for this patient on this date already exists.'
                return render(request, 'vitals_form.html', context)
            
            visit = Visit.objects.create(
                patient=patient,
                visit_date=visit_date,
                height=height_decimal,
                weight=weight_decimal
            )
            
            if visit.bmi > 25:
                return redirect('overweight_assessment', visit_id=visit.id)
            else:
                return redirect('general_assessment', visit_id=visit.id)
                
        except ValueError:
            context['error'] = 'Invalid height or weight value.'
            return render(request, 'vitals_form.html', context)
        except Exception as e:
            context['error'] = f'Error creating visit: {str(e)}'
            return render(request, 'vitals_form.html', context)
    
    return render(request, 'vitals_form.html', context)


@require_http_methods(["GET", "POST"])
def general_assessment(request, visit_id):
    """Handle general assessment form"""
    visit = get_object_or_404(Visit, id=visit_id)
    
    context = {
        'visit': visit,
        'form_data': {},
        'error': None
    }
    
    if visit.bmi > 25:
        context['error'] = 'This visit requires an Overweight Assessment (BMI > 25).'
    
    if request.method == 'POST':
        general_health = request.POST.get('general_health')
        using_drugs = request.POST.get('using_drugs')
        comments = request.POST.get('comments', '').strip()
        
        context['form_data'] = {
            'general_health': general_health,
            'using_drugs': using_drugs,
            'comments': comments
        }
        
        if not all([general_health, using_drugs, comments]):
            context['error'] = 'All fields are required.'
            return render(request, 'general_assessment.html', context)
        
        if visit.bmi > 25:
            context['error'] = 'Cannot submit general assessment for BMI > 25.'
            return render(request, 'general_assessment.html', context)
        
        try:
            Assessment.objects.create(
                visit=visit,
                assessment_type='general',
                general_health=general_health,
                using_drugs=(using_drugs == 'true'),
                comments=comments
            )
            return redirect('patient_listing')
        except Exception as e:
            context['error'] = f'Error creating assessment: {str(e)}'
            return render(request, 'general_assessment.html', context)
    
    return render(request, 'general_assessment.html', context)


@require_http_methods(["GET", "POST"])
def overweight_assessment(request, visit_id):
    """Handle overweight assessment form"""
    visit = get_object_or_404(Visit, id=visit_id)
    
    context = {
        'visit': visit,
        'form_data': {},
        'error': None
    }
    
    if visit.bmi <= 25:
        context['error'] = 'This visit requires a General Assessment (BMI ≤ 25).'
    
    if request.method == 'POST':
        general_health = request.POST.get('general_health')
        on_diet = request.POST.get('on_diet')
        comments = request.POST.get('comments', '').strip()
        
        context['form_data'] = {
            'general_health': general_health,
            'on_diet': on_diet,
            'comments': comments
        }
        
        if not all([general_health, on_diet, comments]):
            context['error'] = 'All fields are required.'
            return render(request, 'overweight_assessment.html', context)
        
        if visit.bmi <= 25:
            context['error'] = 'Cannot submit overweight assessment for BMI ≤ 25.'
            return render(request, 'overweight_assessment.html', context)
        
        try:
            Assessment.objects.create(
                visit=visit,
                assessment_type='overweight',
                general_health=general_health,
                on_diet=(on_diet == 'true'),
                comments=comments
            )
            return redirect('patient_listing')
        except Exception as e:
            context['error'] = f'Error creating assessment: {str(e)}'
            return render(request, 'overweight_assessment.html', context)
    
    return render(request, 'overweight_assessment.html', context)


@require_http_methods(["GET"])
def patient_listing(request):
    """Display patient listing with optional filtering"""
    filter_date = request.GET.get('visit_date')
    
    context = {
        'today': date.today().isoformat(),
        'filter_date': filter_date,
        'patients': [],
        'error': None
    }
    
    try:
        if filter_date:
            patients = Patient.objects.filter(visits__visit_date=filter_date).distinct()
        else:
            patients = Patient.objects.all()
        
        patient_list = []
        for patient in patients:
            latest_visit = patient.get_latest_visit()
            patient_data = {
                'id': patient.id,
                'patient_id': patient.patient_id,
                'first_name': patient.first_name,
                'middle_name': patient.middle_name,
                'last_name': patient.last_name,
                'age': patient.age,
                'last_bmi_status': patient.get_latest_bmi_status(),
                'last_assessment_date': patient.get_latest_assessment_date()
            }
            patient_list.append(patient_data)
        
        context['patients'] = patient_list
        
    except Exception as e:
        context['error'] = f'Error loading patients: {str(e)}'
    
    return render(request, 'patient_listing.html', context)
