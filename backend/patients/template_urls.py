from django.urls import path
from . import template_views

urlpatterns = [
    # Authentication URLs
    path('', template_views.login_view, name='login'),
    path('signup/', template_views.signup_view, name='signup'),
    path('logout/', template_views.logout_view, name='logout'),

    path('listing/', template_views.patient_listing, name='patient_listing'),
    path('register/', template_views.patient_registration, name='patient_registration'),
    path('vitals/<str:patient_id>/', template_views.vitals_form, name='vitals_form'),
    path('assessment/general/<int:visit_id>/', template_views.general_assessment, name='general_assessment'),
    path('assessment/overweight/<int:visit_id>/', template_views.overweight_assessment, name='overweight_assessment'),
]
