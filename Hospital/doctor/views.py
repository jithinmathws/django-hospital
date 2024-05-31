from django.shortcuts import render, redirect, HttpResponse
from .models import DoctorDetails, DoctorDepartment, PatientDetails, GuardianDetails, NurseDetails, PharmacistDetails
from .forms import DepartmentForm, DoctorForm, PatientForm, GuardianForm, NurseForm, PharmacistForm, BedCategoryForm, AddBedForm

from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator, PageNotAnInteger
from django.conf import settings
from django.db.models import Q
from functools import wraps
from tablib import Dataset
from .resources import doctorResources


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
def doctor_add(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Dindex')
    else:
        form = DoctorForm()
    return render(request, "doctor/doctor.html", {'form': form})

@login_required
def doctor_list(request):
    page_size = int(request.GET.get('page_size', getattr(settings, 'PAGE_SIZE', 5)))
    page = request.GET.get('page', 1)

    doctors = DoctorDetails.objects.all()
    paginator = Paginator(doctors, page_size)
    try:
        doctors_page = paginator.page(page)
    except PageNotAnInteger:
        doctors_page = paginator.page(1)
    return render(request, "doctor/doctor_list.html", {'doctors': doctors, 'page_size': page_size})

@login_required
def doctor_edit(request, doctor_id):
    role = DoctorDetails.objects.get(pk=doctor_id)
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
    member = DoctorDetails.objects.get(pk=doctor_id)
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
            value = DoctorDetails(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6],
            )
            value.save()

    return render(request, 'doctor/import.html')

# Patient Fields

@login_required
@user_has_role_or_superuser(['HR', 'SeniorHR', 'Director'])
def patient_index(request):
    return render(request, "patient/index.html", {})

@login_required
def patient_add(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Pindex')
    else:
        form = PatientForm()
    return render(request, "patient/addPatient.html", {'form': form})

@login_required
def patient_list(request):

    patients = PatientDetails.objects.all()
    
    return render(request, "patient/patient_list.html", {'patients': patients})

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

# Nurse Fields

@login_required
@user_has_role_or_superuser(['HR', 'SeniorHR', 'Director'])
def nurse_index(request):
    return render(request, "nurse/index.html", {})

@login_required
def nurse_add(request):
    if request.method == 'POST':
        form = NurseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Nurseindex')
    else:
        form = NurseForm()
    return render(request, "nurse/addNurse.html", {'form': form})

@login_required
def nurse_list(request):

    nurses = NurseDetails.objects.all()
    
    return render(request, "nurse/nurse_list.html", {'nurses': nurses})

#pharmacist
@login_required
@user_has_role_or_superuser(['HR', 'SeniorHR', 'Director'])
def pharmacist_index(request):
    return render(request, "pharmacist/index.html", {})

@login_required
def pharmacist_add(request):
    if request.method == 'POST':
        form = PharmacistForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Pharmacistindex')
    else:
        form = PharmacistForm()
    return render(request, "pharmacist/addPharmacist.html", {'form': form})

@login_required
def bed_index(request):
    return render(request, "assignBed/index.html", {})

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
def bed_add(request):
    if request.method == 'POST':
        form = AddBedForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Bindex')
    else:
        form = AddBedForm()
    return render(request, "assignBed/addBed.html", {'form': form})