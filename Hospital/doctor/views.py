from django.shortcuts import render, redirect, HttpResponse
from .models import DoctorDetails, DoctorDepartment
from .forms import DepartmentForm, DoctorForm

# Create your views here.
def doctor_index(request):
    return render(request, "doctor/index.html", {})

def doctor_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Dindex')
    else:
        form = DepartmentForm()
    return render(request, "doctor/department.html", {'form': form})

def doctor_add(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Dindex')
    else:
        form = DoctorForm()
    return render(request, "doctor/doctor.html", {'form': form})

def doctor_list(request):
    doctors = DoctorDetails.objects.all()
    return render(request, "doctor/doctor_list.html", {'doctors': doctors})