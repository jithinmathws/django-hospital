from django.contrib import admin
from .models import *
import data_wizard
from import_export.admin import ImportExportModelAdmin

class InvoiceInLineAdmin(admin.TabularInline):
    model = InvoiceRelation

class InvoiceRelationAdmin(admin.ModelAdmin):
    inlines = [InvoiceInLineAdmin]

class SubInvoiceInLineAdmin(admin.TabularInline):
    model = SubInvoice

class SubInvoiceAdmin(admin.ModelAdmin):
    inlines = [SubInvoiceInLineAdmin]

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
data_wizard.register(BedCategory)
admin.site.register(BedCategory, ImportExportModelAdmin)
data_wizard.register(AddBed)
admin.site.register(AddBed, ImportExportModelAdmin)

data_wizard.register(MainInvoice, SubInvoice)
admin.site.register(MainInvoice, SubInvoiceAdmin)
data_wizard.register(SubInvoice)
admin.site.register(SubInvoice, ImportExportModelAdmin)

data_wizard.register(InvoiceDetail, InvoiceRelation)
admin.site.register(InvoiceDetail, InvoiceRelationAdmin)



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

data_wizard.register(Cart)
admin.site.register(Cart, ImportExportModelAdmin)

data_wizard.register(CartItem)
admin.site.register(CartItem, ImportExportModelAdmin)