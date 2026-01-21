from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal


class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    patient_id = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        help_text="Unique patient identifier"
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    registration_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-registration_date', '-created_at']
        indexes = [
            models.Index(fields=['patient_id']),
            models.Index(fields=['last_name', 'first_name']),
            models.Index(fields=['-registration_date']),
        ]
    
    def __str__(self):
        return f"{self.patient_id} - {self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
    
    def get_latest_visit(self):
        return self.visits.order_by('-visit_date').first()
    
    def get_latest_bmi_status(self):
        latest_visit = self.get_latest_visit()
        if latest_visit and latest_visit.bmi is not None:
            return latest_visit.get_bmi_status()
        return None
    
    def get_latest_assessment_date(self):
        latest_visit = self.get_latest_visit()
        if latest_visit:
            return latest_visit.visit_date
        return None


class Visit(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='visits'
    )
    visit_date = models.DateField()
    height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('30.0')), MaxValueValidator(Decimal('300.0'))],
        help_text="Height in centimeters"
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('1.0')), MaxValueValidator(Decimal('500.0'))],
        help_text="Weight in kilograms"
    )
    bmi = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Body Mass Index (auto-calculated)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-visit_date', '-created_at']
        indexes = [
            models.Index(fields=['patient', '-visit_date']),
            models.Index(fields=['-visit_date']),
        ]
        unique_together = ['patient', 'visit_date']
    
    def __str__(self):
        return f"{self.patient.patient_id} - Visit on {self.visit_date}"
    
    def calculate_bmi(self):
        if self.height and self.weight:
            height_in_meters = self.height / Decimal('100.0')
            self.bmi = self.weight / (height_in_meters ** 2)
            return self.bmi
        return None
    
    def get_bmi_status(self):
        if self.bmi is None:
            return None
        
        if self.bmi < Decimal('18.5'):
            return 'Underweight'
        elif self.bmi < Decimal('25.0'):
            return 'Normal'
        else:
            return 'Overweight'
    
    def requires_overweight_assessment(self):
        return self.bmi is not None and self.bmi > Decimal('25.0')
    
    def save(self, *args, **kwargs):
        self.calculate_bmi()
        super().save(*args, **kwargs)


class Assessment(models.Model):
    HEALTH_CHOICES = [
        ('Good', 'Good'),
        ('Poor', 'Poor'),
    ]
    
    ASSESSMENT_TYPE_CHOICES = [
        ('general', 'General Assessment'),
        ('overweight', 'Overweight Assessment'),
    ]
    
    visit = models.OneToOneField(
        Visit,
        on_delete=models.CASCADE,
        related_name='assessment'
    )
    assessment_type = models.CharField(
        max_length=20,
        choices=ASSESSMENT_TYPE_CHOICES
    )
    general_health = models.CharField(max_length=10, choices=HEALTH_CHOICES)
    on_diet = models.BooleanField(
        null=True,
        blank=True,
        help_text="For overweight assessment: Have you ever been on a diet to lose weight?"
    )
    using_drugs = models.BooleanField(
        null=True,
        blank=True,
        help_text="For general assessment: Are you currently using any drugs?"
    )
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['visit']),
            models.Index(fields=['assessment_type']),
        ]
    
    def __str__(self):
        return f"{self.assessment_type.title()} - {self.visit.patient.patient_id} on {self.visit.visit_date}"
    
    def clean(self):
        if self.assessment_type == 'overweight':
            if self.on_diet is None:
                raise ValidationError({
                    'on_diet': 'This field is required for overweight assessments.'
                })
            if self.using_drugs is not None:
                raise ValidationError({
                    'using_drugs': 'This field should not be set for overweight assessments.'
                })
        elif self.assessment_type == 'general':
            if self.using_drugs is None:
                raise ValidationError({
                    'using_drugs': 'This field is required for general assessments.'
                })
            if self.on_diet is not None:
                raise ValidationError({
                    'on_diet': 'This field should not be set for general assessments.'
                })
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
