from django.contrib import admin
from .models import *
import data_wizard
from import_export.admin import ImportExportModelAdmin

# Register your models here.

data_wizard.register(DoctorInfo)
admin.site.register(DoctorInfo, ImportExportModelAdmin)
data_wizard.register(CertificateDoctor)
admin.site.register(CertificateDoctor, ImportExportModelAdmin)
admin.site.register(DoctorDepartment)
data_wizard.register(PatientDetails)
admin.site.register(PatientDetails, ImportExportModelAdmin)
data_wizard.register(GuardianDetails)
admin.site.register(GuardianDetails, ImportExportModelAdmin)

data_wizard.register(NurseDetails)
admin.site.register(NurseDetails, ImportExportModelAdmin)
data_wizard.register(AdmissionDetails)
admin.site.register(AdmissionDetails, ImportExportModelAdmin)
data_wizard.register(AppointmentDetails)
admin.site.register(AppointmentDetails, ImportExportModelAdmin)
data_wizard.register(PharmacistDetails)
admin.site.register(PharmacistDetails, ImportExportModelAdmin)
data_wizard.register(BedCategory)
admin.site.register(BedCategory, ImportExportModelAdmin)
data_wizard.register(AddBed)
admin.site.register(AddBed, ImportExportModelAdmin)
data_wizard.register(InvoiceDetails)
admin.site.register(InvoiceDetails, ImportExportModelAdmin)
data_wizard.register(IncomeDetails)
admin.site.register(IncomeDetails, ImportExportModelAdmin)
data_wizard.register(TreatmentDetails)
admin.site.register(TreatmentDetails, ImportExportModelAdmin)