from django.urls import path
from . import views

urlpatterns = [
    path("", views.doctor_index, name="Dindex"),
    path("department/", views.doctor_department, name="department"),
    path("doctor/", views.doctor_add, name="doctor"),
    path("doctorlist/", views.doctor_list, name="doctor_list"),
    path("importDoctor/", views.importDoctorExcel, name="doctorExcel"),

    path("doctor_edit-account/<int:doctor_id>/", views.doctor_edit, name="doctor_edit"),
    path("doctor_delete-account/<int:doctor_id>/", views.doctor_delete, name="doctor_delete"),
    
    path("patient/", views.patient_index, name="Pindex"),
    path("addPatient/", views.patient_add, name="patient"),
    path("patientlist/", views.patient_list, name="patient_list"),
    path("addGuardian/", views.guardian_add, name="guardian"),
    path("guradianlist/", views.guardian_list, name="guardian_list"),

    path("nurse/", views.nurse_index, name="Nurseindex"),
    path("addNurse/", views.nurse_add, name="nurse"),
    path("nurselist/", views.nurse_list, name="nurse_list"),

    path("pharmacist/", views.pharmacist_index, name="Pharmacistindex"),
    path("addPharmacist/", views.pharmacist_add, name="pharmacist"),

    path("bed/", views.bed_index, name="Bindex"),
    path("bedCategory/", views.bed_category, name="bedCategory"),
    path("addBed/", views.bed_add, name="addBed"),
]
