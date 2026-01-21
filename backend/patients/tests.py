from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from datetime import date, timedelta
from .models import Patient, Visit, Assessment


class PatientModelTest(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(
            patient_id='TEST001',
            first_name='John',
            last_name='Doe',
            date_of_birth=date(1990, 1, 1),
            gender='M'
        )
    
    def test_patient_creation(self):
        self.assertEqual(self.patient.patient_id, 'TEST001')
        self.assertEqual(self.patient.full_name, 'John Doe')
    
    def test_patient_age_calculation(self):
        expected_age = date.today().year - 1990
        if date.today() < date(date.today().year, 1, 1):
            expected_age -= 1
        self.assertEqual(self.patient.age, expected_age)
    
    def test_unique_patient_id(self):
        with self.assertRaises(Exception):
            Patient.objects.create(
                patient_id='TEST001',
                first_name='Jane',
                last_name='Doe',
                date_of_birth=date(1995, 1, 1),
                gender='F'
            )


class VisitModelTest(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(
            patient_id='TEST002',
            first_name='Jane',
            last_name='Smith',
            date_of_birth=date(1985, 5, 15),
            gender='F'
        )
    
    def test_bmi_calculation(self):
        visit = Visit.objects.create(
            patient=self.patient,
            visit_date=date.today(),
            height=Decimal('170.00'),
            weight=Decimal('70.00')
        )
        expected_bmi = Decimal('70.00') / (Decimal('1.70') ** 2)
        self.assertAlmostEqual(float(visit.bmi), float(expected_bmi), places=2)
    
    def test_bmi_status_underweight(self):
        visit = Visit.objects.create(
            patient=self.patient,
            visit_date=date.today(),
            height=Decimal('170.00'),
            weight=Decimal('50.00')
        )
        self.assertEqual(visit.get_bmi_status(), 'Underweight')
    
    def test_bmi_status_normal(self):
        visit = Visit.objects.create(
            patient=self.patient,
            visit_date=date.today(),
            height=Decimal('170.00'),
            weight=Decimal('65.00')
        )
        self.assertEqual(visit.get_bmi_status(), 'Normal')
    
    def test_bmi_status_overweight(self):
        visit = Visit.objects.create(
            patient=self.patient,
            visit_date=date.today(),
            height=Decimal('170.00'),
            weight=Decimal('80.00')
        )
        self.assertEqual(visit.get_bmi_status(), 'Overweight')
    
    def test_unique_visit_per_day(self):
        Visit.objects.create(
            patient=self.patient,
            visit_date=date.today(),
            height=Decimal('170.00'),
            weight=Decimal('70.00')
        )
        with self.assertRaises(Exception):
            Visit.objects.create(
                patient=self.patient,
                visit_date=date.today(),
                height=Decimal('175.00'),
                weight=Decimal('75.00')
            )


class AssessmentModelTest(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(
            patient_id='TEST003',
            first_name='Bob',
            last_name='Johnson',
            date_of_birth=date(1980, 3, 20),
            gender='M'
        )
        self.visit = Visit.objects.create(
            patient=self.patient,
            visit_date=date.today(),
            height=Decimal('175.00'),
            weight=Decimal('85.00')
        )
    
    def test_general_assessment_creation(self):
        assessment = Assessment.objects.create(
            visit=self.visit,
            assessment_type='general',
            general_health='Good',
            using_drugs=False,
            comments='Patient is healthy'
        )
        self.assertEqual(assessment.assessment_type, 'general')
        self.assertFalse(assessment.using_drugs)
    
    def test_overweight_assessment_creation(self):
        assessment = Assessment.objects.create(
            visit=self.visit,
            assessment_type='overweight',
            general_health='Good',
            on_diet=True,
            comments='Patient is on a diet'
        )
        self.assertEqual(assessment.assessment_type, 'overweight')
        self.assertTrue(assessment.on_diet)
    
    def test_one_assessment_per_visit(self):
        Assessment.objects.create(
            visit=self.visit,
            assessment_type='overweight',
            general_health='Good',
            on_diet=True,
            comments='First assessment'
        )
        with self.assertRaises(Exception):
            Assessment.objects.create(
                visit=self.visit,
                assessment_type='overweight',
                general_health='Poor',
                on_diet=False,
                comments='Second assessment'
            )
