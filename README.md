# Patient Management System

This is a patient management system built with Django,Python, HTML, and CSS. This system enables healthcare providers to register patients, record vitals with automatic BMI calculation, conduct conditional health assessments, and manage patient records efficiently.


This is a complete healthcare management solution that:
-Registers patients uniquely
-Captures patient vitals with automatic BMI calculation
-Dynamic routing where pages are loaded automatically based on conditions
-Collects additional data after BMI calculation
-Displays patients listing

Features

:Patient Registration
- Unique patient ID validation (prevents duplicates)
- Patients details - name, dob, phone number
- Automatic redirection to vitals form

:Vitals form
-Name of the patient is displayed at the top
- Height (cm) and weight (kg) input with validation
- Automatic BMI Calculation: BMI = weight(kg) / height(m)²
- BMI status display (Underweight, Normal, Overweight)
- Multiple visits per patient with date tracking
- Conditional routing based on BMI values

 Conditional Assessment Forms
- General Assessment(BMI ≤ 25): Captures general health status and drug usage
- Overweight Assessment (BMI > 25): Captures diet history and health status
- Form-specific validation ensures data integrity
- Mandatory comments field for clinical notes

Patient Listing & Filtering
- Comprehensive patient table showing the name, age, BMI, Lastassessment date
- BMI status badges with color coding
- Filter patients by visit date
- Quick access to add new visits
- Age calculation from date of birth

 Technology Stack

 Backend
- Python 3.11+
- Django 4.2.9 - Web framework with template rendering
- Django REST Framework 3.14.0 - RESTful API
- PostgreSQL - Primary database
- django-cors-headers - CORS handling
- django-filter - Advanced filtering

 Frontend
- HTML5 - Format for the website
- CSS3 - Modern styling with custom properties
- Django Templates - Server-side rendering


 Project Structure

PatientManagementSystem/
├── backend/
│   ├── patient_management/          # Django project
│   │   ├── settings.py              # Configuration
│   │   ├── urls.py                  # URL routing
│   │   └── wsgi.py                  
│   ├── patients/                    # Main app
│   │   ├── models.py                # Database models
│   │   ├── template_views.py        # HTML views
│   │   ├── template_urls.py         # HTML routing
│   │   ├── views.py                 # API views
│   │   ├── serializers.py           # API serializers
│   │   ├── admin.py                 # Admin config
│   │   └── templates/               # HTML templates
│   │       ├── base.html
│   │       ├── patient_registration.html
│   │       ├── vitals_form.html
│   │       ├── general_assessment.html
│   │       ├── overweight_assessment.html
│   │       └── patient_listing.html
│   ├── static/
│   │   └── css/
│   │       └── styles.css           # All styling
│   ├── manage.py
│   └── requirements.txt
└── README.md

 API Endpoints
- `/api/patients/` - Patient API
- `/api/visits/` - Visit API
- `/api/assessments/` - Assessment API
- `/admin/` - Django admin interface


 Form Handling
- HTML5 form validation
- Server-side validation with error messages
- Form data persistence on validation errors
- Success messages with auto-redirect
- POST/Redirect/GET pattern


 Data Validation
: Backend Validation
- Model-level constraints (unique patient IDs, date ranges)
- View-level validation (field formats, business rules)
- Custom validators for BMI thresholds
- Database constraints for data integrity

 Frontend Validation
- HTML5 required attributes
- Input type validation (date, number)
- Min/max constraints on numeric fields
- Pattern matching where applicable

 Database Schema
:Patient Model
- `patient_id` (unique, indexed)
- `first_name`, `last_name`
- `date_of_birth`
- `gender` (M/F/O)
- `registration_date` (auto-generated)

:Visit Model
- `patient` (foreign key)
- `visit_date`
- `height` (cm), `weight` (kg)
- `bmi` (auto-calculated)
- Unique constraint: (patient, visit_date)

: Assessment Model
- `visit` (one-to-one)
- `assessment_type` (general/overweight)
- `general_health` (Good/Poor)
- `on_diet` (boolean, overweight only)
- `using_drugs` (boolean, general only)
- `comments` (text)


 Django Admin

Access admin panel at `http://localhost:8000/admin/` with superuser credentials.


How It Works Without JavaScript

:Form Submissions
1. Browser sends POST request to Django view
2. Django validates data server-side
3. On success: Redirect to next page (PRG pattern)
4. On error: Re-render form with error messages

:BMI Calculation
- User enters height and weight
- Form submits to server
- Django calculates BMI in `Visit.save()` method
- User redirected to appropriate assessment form

:Filtering
- Filter form uses GET request
- Django filters queryset based on parameters
- Page re-renders with filtered results

: Navigation
- Standard HTML links
- Form redirects after successful submission
- Browser back button works naturally

