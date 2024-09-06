from django.conf import settings
from django.urls import path
from django.views.static import serve
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.doctor_index, name="Dindex"),
    path("department/", views.doctor_department, name="department"),
    path("departmentlist/", views.department_list, name="department_list"),
    path("department_edit-account/<int:department_id>/", views.department_edit, name="department_edit"),
    path("department_delete-account/<int:department_id>/", views.department_delete, name="department_delete"),

    path("doctor/", views.doctor_add, name="doctor"),
    path("doctorlist/", views.doctor_list, name="doctor_list"),
    path("doctorProfile/<int:doctor_id>/", views.doctor_profile, name="doctor_profile"),
    path("importDoctor/", views.importDoctorExcel, name="doctorExcel"),
    path("exportDoctor/", views.ExportToCsv, name="doctorExportCsv"),
      
    path("doctor_edit-account/<int:doctor_id>/", views.doctor_edit, name="doctor_edit"),
    path("doctor_delete-account/<int:doctor_id>/", views.doctor_delete, name="doctor_delete"),
    
    path("patient/", views.patient_index, name="Pindex"),
    path("addPatient/", views.patient_add, name="patient"),
    
    path("statusPatient/", views.patient_status, name="patient_status"),
    path("admissionPatient/", views.patient_admission, name="patient_admission"),
    path("appointmentPatient/", views.patient_appointment, name="patient_appointment"),
    path("patientlist/", views.patient_list, name="patient_list"),
    path("patientProfile/<int:patient_id>/", views.patient_profile, name="patient_profile"),
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
    path("invoiceItem/", views.invoice_item, name="invoice_item"),
    path("addInvoice/", views.invoice_add, name="invoice"),
    path("create-invoice/", views.invoice_partial, name="create-invoice"),
    path("createInvoice/", views.create_invoice.as_view(), name="create_invoice"),
    path("addIncome/", views.income_add, name="income"),
    path("invoicelist/", views.invoice_list, name="invoice_list"),
    path("incomelist/", views.income_list, name="income_list"),

    path("redirect_me/", views.redirect_me, name="redirect"),

    path("invoiceProfile/<int:invoice_id>/", views.invoice_profile, name="invoice_profile"),
    path("invoice_edit-account/<int:invoice_id>/", views.invoice_edit, name="invoice_edit"),
    path("invoice_delete-account/<int:invoice_id>/", views.invoice_delete, name="invoice_delete"),
    path("income_edit-account/<int:income_id>/", views.income_edit, name="income_edit"),
    path("income_delete-account/<int:income_id>/", views.income_delete, name="income_delete"),

    path("treatment/", views.treatment_index, name="Treatmentindex"),
    path("addTreatment/", views.treatment_add, name="treatment"),
    path("treatmentlist/", views.treatment_list, name="treatment_list"),
    path("treatment_edit-account/<int:treatment_id>/", views.treatment_edit, name="treatment_edit"),
    path("treatment_delete-account/<int:treatment_id>/", views.treatment_delete, name="treatment_delete"),

    path("pharmacy/", views.pharmacy_index, name="Pharmacyindex"),

    
]
