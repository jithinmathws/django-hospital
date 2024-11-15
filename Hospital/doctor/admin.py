from django.contrib import admin
from .models import *
import data_wizard
from import_export.admin import ImportExportModelAdmin

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class StockAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('item_name',)}

class CustomerAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
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

data_wizard.register(Room)
admin.site.register(Room, ImportExportModelAdmin)
data_wizard.register(Booking)
admin.site.register(Booking, ImportExportModelAdmin)
data_wizard.register(Dependees)
admin.site.register(Dependees, ImportExportModelAdmin)
data_wizard.register(Refund)
admin.site.register(Refund, ImportExportModelAdmin)

#old bed models
data_wizard.register(BedCategory)
admin.site.register(BedCategory, ImportExportModelAdmin)
data_wizard.register(AddBed)
admin.site.register(AddBed, ImportExportModelAdmin)
#old bed model ends

data_wizard.register(HospitalService)
admin.site.register(HospitalService, ImportExportModelAdmin)

data_wizard.register(InvoiceData)
admin.site.register(InvoiceData, ImportExportModelAdmin)

data_wizard.register(InvoiceItem)
admin.site.register(InvoiceItem, ImportExportModelAdmin)

data_wizard.register(IncomeDetails)
admin.site.register(IncomeDetails, ImportExportModelAdmin)

data_wizard.register(TreatmentDetails)
admin.site.register(TreatmentDetails, ImportExportModelAdmin)

data_wizard.register(Category)
admin.site.register(Category, CategoryAdmin)

data_wizard.register(Stock)
admin.site.register(Stock, StockAdmin)

data_wizard.register(Customer)
admin.site.register(Customer, CustomerAdmin)

data_wizard.register(CartItem)
admin.site.register(CartItem, ImportExportModelAdmin)