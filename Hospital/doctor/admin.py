from django.contrib import admin
from .models import *
import data_wizard
from import_export.admin import ImportExportModelAdmin

# Register your models here.
data_wizard.register(DoctorDetails)
admin.site.register(DoctorDetails, ImportExportModelAdmin)
admin.site.register(DoctorDepartment)
data_wizard.register(PatientDetails)
admin.site.register(PatientDetails, ImportExportModelAdmin)
admin.site.register(GuardianDetails)
