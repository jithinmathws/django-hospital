from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

# Register your models here.
admin.site.register(DoctorDetails, ImportExportModelAdmin)
admin.site.register(DoctorDepartment)
admin.site.register(PatientDetails, ImportExportModelAdmin)
admin.site.register(GuardianDetails)
