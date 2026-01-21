# Patient Management System

A production-ready patient management system built with Django, HTML, and CSS. This system enables healthcare providers to register patients, record vitals with automatic BMI calculation, conduct conditional health assessments, and manage patient records efficiently.

## 🎯 Overview

This is a complete healthcare management solution that:

- **Registers patients uniquely** with comprehensive demographic information
- **Captures patient vitals** (height, weight) with automatic BMI calculation
- **Routes users dynamically** to appropriate assessment forms based on BMI thresholds
- **Collects conditional assessment data** tailored to patient BMI categories
- **Displays patient listings** with BMI status indicators and date-based filtering
- **Persists all data** via Django ORM with PostgreSQL

## ✨ Key Features

### Patient Registration
- Unique patient ID validation (prevents duplicates)
- Comprehensive demographic capture (name, DOB, gender)
- Server-side validation with error feedback
- Automatic redirection to vitals form

### Vitals Management
- Height (cm) and weight (kg) input with validation
- **Automatic BMI calculation**: BMI = weight(kg) / height(m)²
- BMI status display (Underweight, Normal, Overweight)
- Multiple visits per patient with date tracking
- Conditional routing based on BMI thresholds

### Conditional Assessment Forms
- **General Assessment** (BMI ≤ 25): Captures general health status and drug usage
- **Overweight Assessment** (BMI > 25): Captures diet history and health status
- Form-specific validation ensures data integrity
- Mandatory comments field for clinical notes

### Patient Listing & Filtering
- Comprehensive patient table with key metrics
- BMI status badges with color coding
- Filter patients by visit date
- Quick access to add new visits
- Age calculation from date of birth

## 🛠 Technology Stack

### Backend
- **Python 3.11+**
- **Django 4.2.9** - Web framework with template rendering
- **Django REST Framework 3.14.0** - RESTful API
- **PostgreSQL** - Primary database
- **django-cors-headers** - CORS handling
- **django-filter** - Advanced filtering

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with custom properties
- **Django Templates** - Server-side rendering
- **No JavaScript** - Pure HTML forms with POST/GET requests

## 📋 Prerequisites

- Python 3.11 or higher
- PostgreSQL 14+
- Git

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone <repository-url>
cd PatientManagementSystem
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your PostgreSQL credentials
```

### 3. Database Setup

```bash
# Create PostgreSQL database
psql -U postgres
CREATE DATABASE patient_management_db;
\q

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user (optional)
python manage.py createsuperuser
```

### 4. Start Server

```bash
python manage.py runserver
```

Access at: **http://localhost:8000/**

## 📁 Project Structure

```
PatientManagementSystem/
├── backend/
│   ├── patient_management/          # Django project
│   │   ├── settings.py              # Configuration
│   │   ├── urls.py                  # URL routing
│   │   └── wsgi.py                  # WSGI application
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
```

## 🌐 Application Routes

### HTML Pages
- `/` - Redirects to patient listing
- `/patients/` - Patient listing page
- `/patients/register/` - Patient registration form
- `/patients/vitals/<patient_id>/` - Vitals form
- `/patients/assessment/general/<visit_id>/` - General assessment
- `/patients/assessment/overweight/<visit_id>/` - Overweight assessment

### API Endpoints (Available)
- `/api/patients/` - Patient API
- `/api/visits/` - Visit API
- `/api/assessments/` - Assessment API
- `/admin/` - Django admin interface

## 🎨 Design Features

### Pure HTML/CSS Implementation
- **No JavaScript** - All functionality via HTML forms
- **Server-Side Rendering** - Django templates render dynamic content
- **Modern CSS** - Custom properties, flexbox, grid layout
- **Responsive Design** - Mobile-friendly layouts
- **Accessible** - Semantic HTML, proper form labels
- **Professional Design** - Clean medical application aesthetics

### Form Handling
- HTML5 form validation
- Server-side validation with error messages
- Form data persistence on validation errors
- Success messages with auto-redirect
- POST/Redirect/GET pattern

### Visual Feedback
- Color-coded BMI status badges
- Error alerts with icons
- Success confirmations
- Empty state messages
- Professional medical theme

## 🔒 Data Validation

### Backend Validation
- Model-level constraints (unique patient IDs, date ranges)
- View-level validation (field formats, business rules)
- Custom validators for BMI thresholds
- Database constraints for data integrity

### Frontend Validation
- HTML5 required attributes
- Input type validation (date, number)
- Min/max constraints on numeric fields
- Pattern matching where applicable

## 📊 Database Schema

### Patient Model
- `patient_id` (unique, indexed)
- `first_name`, `last_name`
- `date_of_birth`
- `gender` (M/F/O)
- `registration_date` (auto-generated)

### Visit Model
- `patient` (foreign key)
- `visit_date`
- `height` (cm), `weight` (kg)
- `bmi` (auto-calculated)
- Unique constraint: (patient, visit_date)

### Assessment Model
- `visit` (one-to-one)
- `assessment_type` (general/overweight)
- `general_health` (Good/Poor)
- `on_diet` (boolean, overweight only)
- `using_drugs` (boolean, general only)
- `comments` (text)

## 🔧 Development

### Running Tests

```bash
python manage.py test
```

### Django Admin

Access admin panel at `http://localhost:8000/admin/` with superuser credentials.

### Making Changes

- **HTML Templates**: Edit files in `backend/patients/templates/`
- **CSS Styles**: Edit `backend/static/css/styles.css`
- **Views**: Edit `backend/patients/template_views.py`
- **Models**: Edit `backend/patients/models.py` (requires migrations)

## 🚀 Deployment

### Production Checklist
- Set `DEBUG=False` in `.env`
- Use strong `SECRET_KEY`
- Configure `ALLOWED_HOSTS`
- Run `python manage.py collectstatic`
- Enable HTTPS
- Set up database backups
- Configure monitoring

### Static Files

```bash
python manage.py collectstatic
```

Serve via Nginx or CDN in production.

## 🌟 How It Works Without JavaScript

### Form Submissions
1. Browser sends POST request to Django view
2. Django validates data server-side
3. On success: Redirect to next page (PRG pattern)
4. On error: Re-render form with error messages

### BMI Calculation
- User enters height and weight
- Form submits to server
- Django calculates BMI in `Visit.save()` method
- User redirected to appropriate assessment form

### Filtering
- Filter form uses GET request
- Django filters queryset based on parameters
- Page re-renders with filtered results

### Navigation
- Standard HTML links
- Form redirects after successful submission
- Browser back button works naturally

## 📝 Configuration

### Environment Variables (.env)

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_NAME=patient_management_db
DATABASE_USER=postgres
DATABASE_PASSWORD=your-password
DATABASE_HOST=localhost
DATABASE_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

## 🤝 Contributing

This is a technical assessment project demonstrating HTML/CSS frontend with Django backend.

## 📄 License

Created for technical assessment purposes.

---

**Built with Django, HTML, and CSS - No JavaScript Required! 🎉**
