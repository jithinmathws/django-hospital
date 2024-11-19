from django.conf import settings
from django.urls import path, re_path, include
from django.views.static import serve
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("doctor1/", views.doctor_index, name="Dindex"),
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
    path("addRoom/", views.add_room, name="addRoom"),
    path("roomList/", views.room_list, name="room_list"),
    path("room_edit-account/<int:room_id>/", views.room_edit, name="room_edit"),
    path("room_delete-account/<int:room_id>/", views.room_delete, name="room_delete"),

    path("rooms/", views.rooms, name="bookRoom"),
    path("room_profile/<int:id>/", views.room_profile, name="room_profile"),

    path("booking/", views.bookings, name="booking"),
    path("booking-make/", views.booking_make, name="booking_make"),

    #old bed path
    path("bedCategory/", views.bed_category, name="bedCategory"),
    path("categorylist/", views.category_list, name="category_list"),
    path("bedCategory_edit-account/<int:category_id>/", views.category_edit, name="category_edit"),
    path("bedCategory_delete-account/<int:category_id>/", views.category_delete, name="category_delete"),
    path("addBed/", views.bed_add, name="addBed"),
    #old bed path ends

    path("invoice/", views.invoice_index, name="Invoiceindex"),
    path("addService/", views.add_service, name="add_service"),
    path("Servicelist/", views.service_list, name="service_list"),
    path("service_edit-account/<int:service_id>/", views.service_edit, name="service_edit"),
    path("service_delete-account/<int:service_id>/", views.service_delete, name="service_delete"),

    path("addInvoice/", views.invoice_data, name="invoice_data"),
    path("invoiceAddition/<slug:slug>/", views.invoice_additional_data, name="addition_data"),
    path("invoiceAddlist/", views.invoice_data_list, name="invoice_data_list"),
    path("invoice_edit-account/<int:invoice_id>/", views.invoice_data_edit, name="invoice_data_edit"),
    path("data_delete-account/<int:invoice_id>/", views.invoice_data_delete, name="invoice_data_delete"),

    #old invoice url path

    #old invoice url end

    path("addIncome/", views.income_add, name="income"),
    
    path("incomelist/", views.income_list, name="income_list"),

    #path("redirect_me/", views.redirect_me, name="redirect"),

    
    path("income_edit-account/<int:income_id>/", views.income_edit, name="income_edit"),
    path("income_delete-account/<int:income_id>/", views.income_delete, name="income_delete"),

    path("treatment/", views.treatment_index, name="Treatmentindex"),
    path("addTreatment/", views.treatment_add, name="treatment"),
    path("treatmentlist/", views.treatment_list, name="treatment_list"),
    path("treatment_edit-account/<int:treatment_id>/", views.treatment_edit, name="treatment_edit"),
    path("treatment_delete-account/<int:treatment_id>/", views.treatment_delete, name="treatment_delete"),

    path("pharmacy/", views.pharmacy_index, name="Pharmacyindex"),
    path("inventory/", views.inventory_index, name="Inventoryindex"),
    path("addCategory/", views.add_category, name="category"),
    path("addStock/", views.add_stock, name="stock"),
    path("stockList/", views.stock_list, name="stock_list"),
    path("importStock/", views.importStockExcel, name="stockExcel"),
    path("exportStock/", views.StockToCsv, name="stockExportCsv"),
    path("stockProfile/<int:stock_id>/", views.stock_profile, name="stock_profile"),
    path("recieveStock/<int:stock_id>/", views.recieve_stock, name="recieve_stock"),
    #path("stockLevel/<int:stock_id>/", views.stock_level, name="stock_level"),

    path("stock_edit-account/<int:stock_id>/", views.stock_edit, name="stock_edit"),
    path("stock_delete-account/<int:stock_id>/", views.stock_delete, name="stock_delete"),

    path("stockSale/", views.stock_sale, name="stock_sale"),
    
    path('add_cart/<slug:slug>/', views.add_cart, name="add_cart"),
    path("cart/<slug:slug>/", views.cart, name="cart"),
    path('cart_quantity/<slug:slug>/<int:product_id>/', views.cart_quantity, name="cart_quantity"),
    path('remove_cart/<slug:slug>/<int:product_id>/', views.remove_cart, name="remove_cart"),
    path('delete_cart/<slug:slug>/<int:product_id>/', views.delete_cart, name="delete_cart"),
    
    path("checkout/<slug:slug>/", views.checkout, name="checkout"),
]
