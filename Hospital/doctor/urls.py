from django.urls import path
from . import views

urlpatterns = [
    path("", views.doctor_index, name="Dindex"),
    path("department/", views.doctor_department, name="department"),
    path("departmentlist/", views.department_list, name="department_list"),
    path("department_edit-account/<int:department_id>/", views.department_edit, name="department_edit"),
    path("department_delete-account/<int:department_id>/", views.department_delete, name="department_delete"),

    path("doctor/", views.doctor_add, name="doctor"),
    path("doctorlist/", views.doctor_list, name="doctor_list"),
    path("importDoctor/", views.importDoctorExcel, name="doctorExcel"),
    path("doctor_edit-account/<int:doctor_id>/", views.doctor_edit, name="doctor_edit"),
    path("doctor_delete-account/<int:doctor_id>/", views.doctor_delete, name="doctor_delete"),
    
    path("patient/", views.patient_index, name="Pindex"),
    path("addPatient/", views.patient_add, name="patient"),
    path("statusPatient/", views.patient_status, name="patient_status"),
    path("admissionPatient/", views.patient_admission, name="patient_admission"),
    path("patientlist/", views.patient_list, name="patient_list"),
    path("patient_edit-account/<int:patient_id>/", views.patient_edit, name="patient_edit"),
    path("patient_delete-account/<int:patient_id>/", views.patient_delete, name="patient_delete"),

    path("addGuardian/", views.guardian_add, name="guardian"),
    path("guradianlist/", views.guardian_list, name="guardian_list"),
    path("guardian_edit-account/<int:guardian_id>/", views.guardian_edit, name="guardian_edit"),
    path("guardian_delete-account/<int:guardian_id>/", views.guardian_delete, name="guardian_delete"),

    path("nurse/", views.nurse_index, name="Nurseindex"),
    path("addNurse/", views.nurse_add, name="nurse"),
    path("nurselist/", views.nurse_list, name="nurse_list"),
    path("nurse_edit-account/<int:nurse_id>/", views.nurse_edit, name="nurse_edit"),
    path("nurse_delete-account/<int:nurse_id>/", views.nurse_delete, name="nurse_delete"),

    path("pharmacist/", views.pharmacist_index, name="Pharmacistindex"),
    path("addPharmacist/", views.pharmacist_add, name="pharmacist"),
    path("pharmacistlist/", views.pharmacist_list, name="pharmacist_list"),
    path("pharmacist_edit-account/<int:pharmacist_id>/", views.pharmacist_edit, name="pharmacist_edit"),
    path("pharmacist_delete-account/<int:pharmacist_id>/", views.pharmacist_delete, name="pharmacist_delete"),

    path("bed/", views.bed_index, name="Bindex"),
    path("bedCategory/", views.bed_category, name="bedCategory"),
    path("categorylist/", views.category_list, name="category_list"),
    path("bedCategory_edit-account/<int:category_id>/", views.category_edit, name="category_edit"),
    path("bedCategory_delete-account/<int:category_id>/", views.category_delete, name="category_delete"),
    path("addBed/", views.bed_add, name="addBed"),

    path("invoice/", views.invoice_index, name="Invoiceindex"),
    path("addInvoice/", views.invoice_add, name="invoice"),
]
