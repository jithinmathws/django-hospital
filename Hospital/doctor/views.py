from io import BytesIO
from docx import Document

import os
import csv
import base64
import logging

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, HttpResponse

from .models import *
from .forms import *
from .resources import doctorResources

from crispy_forms.helper import FormHelper
from django.forms import formset_factory
from django.forms.models import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import (
    CreateView, UpdateView
)
from django.db import transaction, IntegrityError

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger
from django.conf import settings
from django.db.models import Q, Max
from functools import wraps
from tablib import Dataset


# Create your views here.

# Doctor Fields

def user_has_role_or_superuser(roles):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            user_groups = request.user.groups.all().values_list('name', flat=True)

            if request.user.is_superuser or any(role in user_groups for role in roles):
                return view_func(request, *args, **kwargs)
            else:
                return redirect('Home')
        return _wrapped_view
    return decorator


@login_required
@user_has_role_or_superuser(['HR', 'SeniorHR', 'Director'])
def doctor_index(request):
    return render(request, "doctor/index.html", {})

@login_required
def doctor_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Dindex')
    else:
        form = DepartmentForm()
    return render(request, "doctor/department.html", {'form': form})

@login_required
def department_list(request):
    departments = DoctorDepartment.objects.all()
    return render(request, "doctor/department_list.html", {'departments': departments})

@login_required
def department_edit(request, department_id):
    role = DoctorDepartment.objects.get(pk=department_id)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=role)
        if form.is_valid():
            role = form.save()
            return redirect('department_list')

    else:
        form = DepartmentForm(instance=role)
    return render(request, 'doctor/department_edit.html', {'form': form, 'role': role})

@login_required
def department_delete(request, department_id):
    member = DoctorDepartment.objects.get(pk=department_id)
    member.delete()
    return redirect('department_list')

@login_required
def doctor_add(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES)
        certificate_files = request.FILES.getlist('certificate[]')
        if form.is_valid():
            #doctor = form.save()

            doctor = form.save(commit=False)
            image_blob = request.FILES.get('image')
            if image_blob:
                doctor.image = image_blob.read()

            doctor.save()

            if len(certificate_files)> 15:
                messages.error(request, 'You can only upload a maximum of 15 certificates.')
               
            
            for file in certificate_files:
                CertificateDoctor.objects.create(
                    doctor=doctor,
                    certificate_file = file,
                )
            return redirect('Dindex')
    else:
        form = DoctorForm()
    return render(request, "doctor/doctor.html", {'form': form})

@login_required
def doctor_list(request):
    page_size = int(request.GET.get('page_size', getattr(settings, 'PAGE_SIZE', 5)))
    page = request.GET.get('page', 1)

    search_query = request.GET.get('search', '')

    doctors = DoctorInfo.objects.filter(
        Q(id__icontains=search_query) |
        Q(doctor_name__icontains=search_query) |
        Q(email__icontains=search_query) |
        Q(phone_number__icontains=search_query) 
    )

    doctor_data = []
    for doctor in doctors:
        existing_certificates = len(CertificateDoctor.objects.filter(doctor=doctor))
        remaining_certificates = 10 - existing_certificates
        doctor_data.append({'doctor': doctor, 'remaining_certificates': remaining_certificates})

    paginator = Paginator(doctor_data, page_size)
    try:
        doctors_page = paginator.page(page)
    except PageNotAnInteger:
        doctors_page = paginator.page(1)
    return render(request, "doctor/doctor_list.html", {'doctors_page': doctors_page, 'page_size': page_size, 'search_query': search_query})

@login_required
def doctor_profile(request, doctor_id):
    doctor = get_object_or_404(DoctorInfo, pk=doctor_id)
    certificates = CertificateDoctor.objects.filter(doctor=doctor)

    image_base64 = base64.b64encode(doctor.image).decode('utf-8') if doctor.image else None

    return render(request, "doctor/doctor_profile.html", {'doctor': doctor, 'image_base64': image_base64, 'certificates': certificates})

@login_required
def doctor_edit(request, doctor_id):
    role = DoctorInfo.objects.get(pk=doctor_id)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=role)
        if form.is_valid():
            role = form.save()
            return redirect('doctor_list')

    else:
        form = DoctorForm(instance=role)
    return render(request, 'doctor/doctor_edit.html', {'form': form, 'role': role})

@login_required
def doctor_delete(request, doctor_id):
    member = DoctorInfo.objects.get(pk=doctor_id)
    member.delete()
    return redirect('doctor_list')

@login_required
def importDoctorExcel(request):
    if request.method == 'POST':
        doctor_resource = doctorResources()
        dataset = Dataset()
        new_doctors = request.FILES['my_file']
        imported_data = dataset.load(new_doctors.read(), format='xlsx')
        for data in imported_data:
            value = DoctorInfo(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6],
                data[7],
                data[8],
                data[9],
                data[10],
                data[11],
                data[12],
                data[13],
                data[14],
                data[15]
            )
            value.save()

    return render(request, 'doctor/import.html')

@login_required
def ExportToCsv(request):
    doctors = DoctorInfo.objects.all()
    file_name = f"doctor_data.csv"
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    writer = csv.writer(response)
    writer.writerow(['doctor_id', 'doctor_name', 'department_name', 'date_of_birth', 'gender', 'email', 'phone_number'])
    for doctor in doctors:
        writer.writerow([doctor.id, doctor.doctor_name, doctor.department_name, doctor.date_of_birth, doctor.gender, doctor.email, doctor.phone_number])
    
    return response

# Patient Fields

@login_required
def patient_index(request):
    return render(request, "patient/index.html", {})

'''
@login_required
def patient_example(request):
    number = 1001 if PatientNumber.objects.count() == 0 else PatientNumber.objects.aggregate(max=Max('patient_number'))["max"] + 1
    if request.method == 'POST':
        
        try:
            data = PatientDetails.objects.create(patient_number=number)
            data.save()
        except ObjectDoesNotExist:
            pass
    return render(request, "patient/example.html", locals())
'''

@login_required
def patient_add(request):
    patient_number = 1001 if PatientDetails.objects.count() == 0 else PatientDetails.objects.aggregate(max=Max('patient_number'))["max"] + 1
    form = PatientForm(request.POST or None)
    context = {'form': form, 'patient_number': patient_number}
    if form.is_valid():
        #form.save()
        patient = form.save(commit=False)
        image_blob = request.FILES.get('patient_image')
        image = patient.patient_image
        if image_blob:
            image = image_blob.read()
        patient_name = request.POST['patient_name']
        gender = request.POST['gender']
        blood_group = request.POST['blood_group']
        address = request.POST['address']
        state = request.POST['state']
        country = request.POST['country']
        pin_code = request.POST['pin_code']
        email = request.POST['email']
        date_of_birth = request.POST['date_of_birth']
        phone_number = request.POST['phone_number']
        try:
            data = PatientDetails.objects.create(patient_number=patient_number, patient_name=patient_name, gender=gender, blood_group=blood_group, address=address, state=state, country=country, pin_code=pin_code, email=email, date_of_birth=date_of_birth, phone_number=phone_number, patient_image=image)
            data.save()
        except ObjectDoesNotExist:
            pass
        #patient.save()
        return redirect('Pindex')
    
    
    return render(request, "patient/addPatient.html", context)

@login_required
def patient_status(request):
    if request.method == 'POST':
        form = PatientStatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Pindex')
    else:
        form = PatientStatusForm()
    return render(request, "patient/patient_status.html", {'form': form})

@login_required
def patient_admission(request):
    if request.method == 'POST':
        form = AdmissionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Pindex')
    else:
        form = AdmissionForm()
    return render(request, "patient/patient_admission.html", {'form': form})

@login_required
def patient_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Pindex')
    else:
        form = AppointmentForm()
    return render(request, "patient/patient_appointment.html", {'form': form})

@login_required
def patient_list(request):
    page_size = int(request.GET.get('page_size', getattr(settings, 'PAGE_SIZE', 5)))
    page = request.GET.get('page', 1)

    search_query = request.GET.get('search', '')

    patients = PatientDetails.objects.filter(
        Q(id__icontains=search_query) |
        Q(patient_name__icontains=search_query) |
        Q(email__icontains=search_query) |
        Q(phone_number__icontains=search_query) 
    )

    paginator = Paginator(patients, page_size)
    try:
        patient_page = paginator.page(page)
    except PageNotAnInteger:
        patient_page = paginator.page(1)
    return render(request, "patient/patient_list.html", {'patient_page': patient_page, 'page_size': page_size, 'search_query': search_query})

@login_required
def patient_profile(request, patient_id):
    patient = get_object_or_404(PatientDetails, pk=patient_id)
    
    image_base64 = base64.b64encode(patient.patient_image).decode('utf-8') if patient.patient_image else None

    return render(request, "patient/patient_profile.html", {'patient': patient, 'image_base64': image_base64})

@login_required
def patient_edit(request, patient_id):
    role = PatientDetails.objects.get(pk=patient_id)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=role)
        if form.is_valid():
            role = form.save()
            return redirect('patient_list')

    else:
        form = PatientForm(instance=role)
    return render(request, 'patient/patient_edit.html', {'form': form, 'role': role})

@login_required
def patient_delete(request, patient_id):
    member = PatientDetails.objects.get(pk=patient_id)
    member.delete()
    return redirect('patient_list')

@login_required
def guardian_add(request):
    if request.method == 'POST':
        form = GuardianForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Pindex')
    else:
        form = GuardianForm()
    return render(request, "patient/addGuardian.html", {'form': form})

@login_required
def guardian_list(request):

    guardians = GuardianDetails.objects.all()
    
    return render(request, "patient/guardian_list.html", {'guardians': guardians})

@login_required
def guardian_delete(request, guardian_id):
    member = GuardianDetails.objects.get(pk=guardian_id)
    member.delete()
    return redirect('guardian_list')

@login_required
def guardian_edit(request, guardian_id):
    role = GuardianDetails.objects.get(pk=guardian_id)
    if request.method == 'POST':
        form = GuardianForm(request.POST, instance=role)
        if form.is_valid():
            role = form.save()
            return redirect('guardian_list')

    else:
        form = GuardianForm(instance=role)
    return render(request, 'patient/guardian_edit.html', {'form': form, 'role': role})

# Nurse Fields

@login_required
@user_has_role_or_superuser(['HR', 'SeniorHR', 'Director'])
def nurse_index(request):
    return render(request, "nurse/index.html", {})

@login_required
def nurse_add(request):
    if request.method == 'POST':
        form = NurseForm(request.POST, request.FILES)
        if form.is_valid():
            #form.save()
            nurse = form.save(commit=False)
            image_blob = request.FILES.get('nurse_image')
            if image_blob:
                nurse.nurse_image = image_blob.read()

            nurse.save()
            return redirect('Nurseindex')
    else:
        form = NurseForm()
    return render(request, "nurse/addNurse.html", {'form': form})

@login_required
def nurse_list(request):
    page_size = int(request.GET.get('page_size', getattr(settings, 'PAGE_SIZE', 5)))
    page = request.GET.get('page', 1)

    search_query = request.GET.get('search', '')

    nurses = NurseDetails.objects.filter(
        Q(id__icontains=search_query) |
        Q(nurse_name__icontains=search_query) |
        Q(email__icontains=search_query) |
        Q(phone_number__icontains=search_query) 
    )

    paginator = Paginator(nurses, page_size)
    try:
        nurse_page = paginator.page(page)
    except PageNotAnInteger:
        nurse_page = paginator.page(1)
    
    return render(request, "nurse/nurse_list.html", {'nurse_page': nurse_page, 'page_size': page_size, 'search_query': search_query})

@login_required
def nurse_edit(request, nurse_id):
    role = NurseDetails.objects.get(pk=nurse_id)
    if request.method == 'POST':
        form = NurseForm(request.POST, instance=role)
        if form.is_valid():
            role = form.save()
            return redirect('nurse_list')
    else:
        form = NurseForm(instance=role)
    return render(request, 'nurse/nurse_edit.html', {'form': form, 'role': role})

@login_required
def nurse_delete(request, nurse_id):
    member = NurseDetails.objects.get(pk=nurse_id)
    member.delete()
    return redirect('nurse_list')

#pharmacist
@login_required
@user_has_role_or_superuser(['HR', 'SeniorHR', 'Director'])
def pharmacist_index(request):
    return render(request, "pharmacist/index.html", {})

@login_required
def pharmacist_add(request):
    if request.method == 'POST':
        form = PharmacistForm(request.POST, request.FILES)
        if form.is_valid():
            #form.save()
            pharmacist = form.save(commit=False)
            image_blob = request.FILES.get('pharmacist_image')
            if image_blob:
                pharmacist.pharmacist_image = image_blob.read()

            pharmacist.save()
            return redirect('Pharmacistindex')
    else:
        form = PharmacistForm()
    return render(request, "pharmacist/addPharmacist.html", {'form': form})

@login_required
def pharmacist_list(request):
    page_size = int(request.GET.get('page_size', getattr(settings, 'PAGE_SIZE', 5)))
    page = request.GET.get('page', 1)

    search_query = request.GET.get('search', '')

    pharmacists = PharmacistDetails.objects.filter(
        Q(id__icontains=search_query) |
        Q(pharmacist_name__icontains=search_query) |
        Q(email__icontains=search_query) |
        Q(phone_number__icontains=search_query) 
    )

    paginator = Paginator(pharmacists, page_size)
    try:
        pharmacist_page = paginator.page(page)
    except PageNotAnInteger:
        pharmacist_page = paginator.page(1)
    return render(request, "pharmacist/pharmacist_list.html", {'pharmacist_page': pharmacist_page, 'page_size': page_size, 'search_query': search_query})

@login_required
def pharmacist_edit(request, pharmacist_id):
    role = PharmacistDetails.objects.get(pk=pharmacist_id)
    if request.method == 'POST':
        form = PharmacistForm(request.POST, instance=role)
        if form.is_valid():
            role = form.save()
            return redirect('nurse_list')
    else:
        form = PharmacistForm(instance=role)
    return render(request, 'pharmacist/pharmacist_edit.html', {'form': form, 'role': role})

@login_required
def pharmacist_delete(request, pharmacist_id):
    member = PharmacistDetails.objects.get(pk=pharmacist_id)
    member.delete()
    return redirect('pharmacist_list')

#Assign old Bed view

@login_required
def bed_category(request):
    if request.method == 'POST':
        form = BedCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Bindex')
    else:
        form = BedCategoryForm()
    return render(request, "assignBed/bedcategory.html", {'form': form})

@login_required
def category_list(request):
    categories = BedCategory.objects.all()
    return render(request, "assignBed/bedcategory_list.html", {'categories': categories})

@login_required
def category_edit(request, category_id):
    role = BedCategory.objects.get(pk=category_id)
    if request.method == 'POST':
        form = BedCategoryForm(request.POST, instance=role)
        if form.is_valid():
            role = form.save()
            return redirect('category_list')
    else:
        form = BedCategoryForm(instance=role)
    return render(request, 'assignBed/bedCategory_edit.html', {'form': form, 'role': role})

@login_required
def category_delete(request, category_id):
    member = BedCategory.objects.get(pk=category_id)
    member.delete()
    return redirect('category_list')

@login_required
def bed_add(request):
    if request.method == 'POST':
        form = AddBedForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Bindex')
    else:
        form = AddBedForm()
    return render(request, "assignBed/addBed.html", {'form': form})
#ends old bed

#new room/bed views
@login_required
def bed_index(request):
    return render(request, "assignBed/index.html", {})

@login_required
def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Bindex')
    else:
        form = RoomForm()
    return render(request, "assignBed/addRoom.html", {'form': form})

@login_required
def room_list(request):
    room = Room.objects.all()
    return render(request, "assignBed/room_list.html", {'room': room})

#invoice
@login_required
def invoice_index(request):
    return render(request, "invoice/index.html", {})

#new invoice
@login_required
def add_service(request):
    form = ServiceForm(request.POST or None)
    context = { 'form': form }
    if form.is_valid():
        form.save()
        return redirect('Invoiceindex')
    
    return render(request, "invoice/addservice.html", context)

@login_required
def service_list(request):
    services = HospitalService.objects.all()
    return render(request, "invoice/service_list.html", {'services': services})

@login_required
def service_edit(request, service_id):
    role = HospitalService.objects.get(pk=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=role)
        if form.is_valid():
            role = form.save()
            return redirect('service_list')
    else:
        form = ServiceForm(instance=role)
    return render(request, 'invoice/service_edit.html', {'form': form, 'role': role})

@login_required
def service_delete(request, service_id):
    member = HospitalService.objects.get(pk=service_id)
    member.delete()
    return redirect('service_list')


@login_required
def invoice_data(request):
    #invoice_number = 1001 if InvoiceData.objects.count() == 0 else InvoiceData.objects.aggregate(max=Max('invoice_number'))["max"]+1
    form = InvoiceDataForm(request.POST or None)
    context = { 'form': form }
    if form.is_valid():
        invoice_object = form.save()
        context['form'] = InvoiceDataForm()
        
        return redirect('addition_data', slug=invoice_object.slug)
    
    return render(request, "invoice/invoiceData.html", context)

@login_required
def invoice_additional_data(request, slug):
    invoice = InvoiceData.objects.get(slug=slug)
    context = { 'invoice': invoice }

    return render(request, "invoice/invoiceAddData.html", context)

@login_required
def invoice_data_list(request):
    invoice = InvoiceData.objects.all()
    return render(request, "invoice/invoice_data_list.html", {'invoice': invoice})

@login_required
def invoice_data_edit(request, invoice_id):
    role = InvoiceData.objects.get(pk=invoice_id)
    if request.method == 'POST':
        form = InvoiceDataForm(request.POST, instance=role)
        if form.is_valid():
            role = form.save()
            return redirect('invoice_data_list')
    else:
        form = InvoiceDataForm(instance=role)
    return render(request, 'invoice/invoice_data_edit.html', {'form': form, 'role': role})

@login_required
def invoice_data_delete(request, invoice_id):
    member = InvoiceData.objects.get(pk=invoice_id)
    member.delete()
    return redirect('invoice_data_list')

'''
@login_required
def invoice_additional_data(request, slug):
    invoice = InvoiceData.objects.get(slug=slug)
    form = AddDataForm(request.POST or None)
    context = { 'form': form, 'invoice': invoice }
    if form.is_valid():
        invoice_object = form.save()
        context['form'] = AddDataForm()
        return redirect('Invoiceindex')
        #return redirect('add_cart', slug=invoice_object.slug)
    
    return render(request, "invoice/invoiceAddData.html", context)
'''
    
#manytomany objects.create
'''
    invoice_number = 1001 if InvoiceData.objects.count() == 0 else InvoiceData.objects.aggregate(max=Max('invoice_number'))["max"] + 1
        patient = request.POST['patient']
        services = request.POST['service']
        date = request.POST['date']

        service = HospitalService.objects.filter(pk__in=services)

        try:
            #item = InvoiceData.objects.create(invoice_number=invoice_number, patient=PatientDetails.objects.get(pk=patient), date=date)
            item = InvoiceData.objects.create(patient=PatientDetails.objects.get(pk=patient), date=date)
            for data in service:
                item.service.add(data)

            item.save()
        except ObjectDoesNotExist:
            pass
        #return redirect('Invoiceindex')
        '''

#end new invoice


#old invoice system

#end old invoice




#income
@login_required
def income_add(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Invoiceindex')
    else:
        form = IncomeForm()
    return render(request, "invoice/addIncome.html", {'form': form})

@login_required
def income_list(request):
    incomes = IncomeDetails.objects.all()
    return render(request, "invoice/income_list.html", {'incomes': incomes})

@login_required
def income_edit(request, income_id):
    role = IncomeDetails.objects.get(pk=income_id)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=role)
        if form.is_valid():
            role = form.save()
            return redirect('income_list')
    else:
        form = InvoiceForm(instance=role)
    return render(request, 'invoice/income_edit.html', {'form': form, 'role': role})

@login_required
def income_delete(request, income_id):
    member = IncomeDetails.objects.get(pk=income_id)
    member.delete()
    return redirect('income_list')

#Treatment
@login_required
def treatment_index(request):
    return render(request, "treatment/index.html", {})

@login_required
def treatment_add(request):
    if request.method == 'POST':
        form = TreatmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Treatmentindex')
    else:
        form = TreatmentForm()
    return render(request, "treatment/addTreatment.html", {'form': form})

@login_required
def treatment_list(request):
    treatments = TreatmentDetails.objects.all()
    return render(request, "treatment/treatment_list.html", {'treatments': treatments})

@login_required
def treatment_edit(request, treatment_id):
    role = TreatmentDetails.objects.get(pk=treatment_id)
    if request.method == 'POST':
        form = TreatmentForm(request.POST, instance=role)
        if form.is_valid():
            role = form.save()
            return redirect('treatment_list')

    else:
        form = TreatmentForm(instance=role)
    return render(request, 'treatment/treatment_edit.html', {'form': form, 'role': role})

@login_required
def treatment_delete(request, treatment_id):
    member = TreatmentDetails.objects.get(pk=treatment_id)
    member.delete()
    return redirect('treatment_list')

#Pharmacy
@login_required
def pharmacy_index(request):
    return render(request, "pharmaceuticals/index.html", {})

@login_required
def inventory_index(request):
    return render(request, "pharmaceuticals/inventory_index.html", {})

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Inventoryindex')
    else:
        form = CategoryForm()
    return render(request, "pharmaceuticals/category.html", {'form': form})

@login_required
def add_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Inventoryindex')
    else:
        form = StockForm()
    return render(request, "pharmaceuticals/add_stock.html", {'form': form})

@login_required

@login_required
def stock_list(request):
    page_size = int(request.GET.get('page_size', getattr(settings, 'PAGE_SIZE', 5)))
    page = request.GET.get('page', 1)

    search_query = request.GET.get('search', '')
    
    sort_by = request.GET.get('sort_by', 'id')
    sort_order = request.GET.get('sort_order', 'asc')

    valid_sort_fields = ['id', 'item_name', 'category', 'price', 'stock', 'created', 'last_updated']
    if sort_by not in valid_sort_fields:
        sort_by = 'id'
    
    items = Stock.objects.filter(
        Q(id__icontains=search_query),
        Q(item_name__icontains=search_query)
         
    )


    if sort_order == 'desc':
        items = items.order_by(f'-{sort_by}')
    else:
        items = items.order_by(sort_by)
    
    paginator = Paginator(items, page_size)
    try:
        stock_page = paginator.page(page)
    except PageNotAnInteger:
        stock_page = paginator.page(1)
    
    context = {
        'stock_page': stock_page,
        'page_size': page_size,
        'search_query': search_query,
        'sort_by': sort_by,
        'sort_order': sort_order,
        }
    return render(request, "pharmaceuticals/stock_list.html", context)

@login_required
def importStockExcel(request):
    if request.method == 'POST':
        stock_resource = stockResources()
        dataset = Dataset()
        new_stock = request.FILES['my_file']
        imported_data = dataset.load(new_stock.read(), format='xlsx')
        for data in imported_data:
            value = Stock(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6],
                data[7],
                data[8],
                data[9],
                data[10]
            )
            value.save()

    return render(request, 'pharmaceuticals/import.html')

@login_required
def StockToCsv(request):
    stocks = Stock.objects.all()
    file_name = f"stock_data.csv"
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    writer = csv.writer(response)
    writer.writerow(['stock_id', 'item_name', 'description', 'category', 'price', 'stock'])
    for stock in stocks:
        writer.writerow([stock.id, stock.item_name, stock.description, stock.category, stock.price, stock.stock])
    
    return response

@login_required
def stock_profile(request, stock_id):
    stock = get_object_or_404(Stock, pk=stock_id)

    return render(request, "pharmaceuticals/stock_profile.html", {'stock': stock})

@login_required
def recieve_stock(request, stock_id):
    queryset = Stock.objects.get(id=stock_id)
    form = StockRecieveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.stock += instance.reorder_stock
        instance.save()

        return redirect('stock_list')

    context = {
        'title' : 'Recieved' + str(queryset.item_name),
        'instance' : queryset,
        'form' : form,
    }
    return render(request, 'pharmaceuticals/stock_quantity.html', context)

@login_required
def stock_edit(request, stock_id):
    role = Stock.objects.get(pk=stock_id)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=role)
        if form.is_valid():
            role = form.save()
            return redirect('stock_list')

    else:
        form = StockUpdateForm(instance=role)
    return render(request, 'pharmaceuticals/stock_edit.html', {'form': form, 'role': role})

@login_required
def stock_level(request, stock_id):
    stock = Stock.objects.get(pk=stock_id)
    if request.method == 'POST':
        form = StockLevelForm(request.POST, instance=stock)
        if form.is_valid():
            role = form.save()
            return redirect('stock_list')

    else:
        form = StockLevelForm(instance=stock)
    return render(request, 'pharmaceuticals/stock_edit.html', {'form': form, 'stock': stock})

@login_required
def stock_delete(request, stock_id):
    member = Stock.objects.get(pk=stock_id)
    member.delete()
    return redirect('stock_list')

@login_required
def stock_sale(request):
    form = CustomerForm(request.POST or None)
    context = { 'form': form }
    if form.is_valid():
        customer_object = form.save()
        context['form'] = CustomerForm()
        return redirect('add_cart', slug=customer_object.slug)
    
    return render(request, "pharmaceuticals/sale.html", {'form': form})

@login_required
def add_cart(request, slug):
    customer = Customer.objects.get(slug=slug)
    products = customer.products.all()
    
    for product in products:
        cart_items = CartItem.objects.get(customer=customer, product=product)
        cart_id = cart_items.id
        try:
            cart_item = CartItem.objects.get(id=cart_id)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                customer = customer,
                product = product,
                quantity = 1,
            )
            cart_item.save()
           
    return redirect('cart', slug=customer.slug)

@login_required
def cart_quantity(request, slug, product_id):
    customer = Customer.objects.get(slug=slug)
    product = Stock.objects.get(pk=product_id)
    cart_item = CartItem.objects.get(customer=customer, product=product)
    cart_id = cart_item.id
    try:
        cart = CartItem.objects.get(id=cart_id)
        cart.quantity += 1
        cart.save()
    except CartItem.DoesNotExist:
        cart = CartItem.objects.create(
            customer = customer,
            product = product,
            quantity = 1,
        )
        cart.save()
    return redirect('cart', slug=customer.slug)

@login_required
def remove_cart(request, slug, product_id):
    customer = Customer.objects.get(slug=slug)
    product = Stock.objects.get(pk=product_id)
    cart_item = CartItem.objects.get(customer=customer, product=product)
    cart_id = cart_item.id
    cart = CartItem.objects.get(id=cart_id)
    if cart.quantity > 1:
        cart.quantity -= 1
        cart.save()
    else:
        cart.delete()
    return redirect('cart', slug=customer.slug)

@login_required
def delete_cart(request, slug, product_id):
    customer = Customer.objects.get(slug=slug)
    product = Stock.objects.get(pk=product_id)
    cart_item = CartItem.objects.get(customer=customer, product=product)
    cart_id = cart_item.id
    cart = CartItem.objects.get(id=cart_id)
    cart.delete()
    return redirect('cart', slug=customer.slug)

@login_required
def cart(request, slug, total=0, quantity=0, cart_item=None):
    
    customer = Customer.objects.get(slug=slug)
    products = customer.products.all()
    for product in products:
        cart_items = CartItem.objects.get(customer=customer, product=product, is_active=True)
        cart_id = cart_items.id
        try:
            cart_item = CartItem.objects.get(id=cart_id)
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        except CartItem.DoesNotExist:
                total = quantity = cart_items = None
    entire_cart = CartItem.objects.filter(customer=customer)
    context = {
        'total': total,
        'quantity': quantity,
        'entire_cart': entire_cart,
        'products': products,
        'customer': customer,
    }
    return render(request , "pharmaceuticals/cart.html", context)

@login_required
def checkout(request, slug, total=0, quantity=0):
    customer = Customer.objects.get(slug=slug)
    products = customer.products.all()
    for product in products:
        cart_items = CartItem.objects.get(customer=customer, product=product, is_active=True)
        cart_id = cart_items.id
        cart_item = CartItem.objects.get(id=cart_id)
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    entire_cart = CartItem.objects.filter(customer=customer)
    context = {
        'total': total,
        'quantity': quantity,
        'cart_item': entire_cart,
        'customer': customer,
        }
    return render(request , "pharmaceuticals/checkout.html", context)