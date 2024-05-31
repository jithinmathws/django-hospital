from django import forms


import django.forms.utils
import django.forms.widgets

from .models import DoctorDepartment, DoctorDetails, PatientDetails, GuardianDetails, NurseDetails, PharmacistDetails, BedCategory, AddBed

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = DoctorDepartment
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            print(field)
            new_data = {
                "label": '',
                
                "class": 'form-control'

            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )

class DoctorForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={"type": 'date'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"type": 'email'}))
    class Meta:
        model = DoctorDetails
        fields = ['doctor_name', 'department_name', 'date_of_birth', 'gender', 'email', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            print(field)
        self.fields["doctor_name"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["department_name"].widget.attrs.update({"class": 'form-control'})
        self.fields["date_of_birth"].widget.attrs.update({"class": 'form-control', "type": 'date'})
        self.fields["gender"].widget.attrs.update({"class": 'form-control'})
        self.fields["email"].widget.attrs.update({"class": 'form-control', "type": 'email'})
        self.fields["phone_number"].widget.attrs.update({"class": 'form-control', "type": 'text'})
            

class PatientForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={"type": 'date'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"type": 'email'}))
    class Meta:
        model = PatientDetails
        fields = ['patient_name',  'gender', 'email', 'date_of_birth', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            print(field)
        self.fields["patient_name"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["gender"].widget.attrs.update({"class": 'form-control'})
        self.fields["email"].widget.attrs.update({"class": 'form-control', "type": 'email'})
        self.fields["date_of_birth"].widget.attrs.update({"class": 'form-control', "type": 'date'})
        self.fields["phone_number"].widget.attrs.update({"class": 'form-control', "type": 'text'})
                                
class GuardianForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={"type": 'date'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"type": 'email'}))
    class Meta:
        model = GuardianDetails
        fields = ['guardian_name', 'patient_name', 'gender', 'email', 'date_of_birth', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["guardian_name"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["patient_name"].widget.attrs.update({"class": 'form-control'})
        self.fields["gender"].widget.attrs.update({"class": 'form-control'})
        self.fields["email"].widget.attrs.update({"class": 'form-control', "type": 'email'})
        self.fields["date_of_birth"].widget.attrs.update({"class": 'form-control', "type": 'date'})
        self.fields["phone_number"].widget.attrs.update({"class": 'form-control', "type": 'text'})

class NurseForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={"type": 'date'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"type": 'email'}))
    class Meta:
        model = NurseDetails
        fields = ['nurse_name',  'gender', 'email', 'date_of_birth', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            print(field)
        self.fields["nurse_name"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["gender"].widget.attrs.update({"class": 'form-control'})
        self.fields["email"].widget.attrs.update({"class": 'form-control', "type": 'email'})
        self.fields["date_of_birth"].widget.attrs.update({"class": 'form-control', "type": 'date'})
        self.fields["phone_number"].widget.attrs.update({"class": 'form-control', "type": 'text'})

class PharmacistForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={"type": 'date'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"type": 'email'}))
    class Meta:
        model = PharmacistDetails
        fields = ['pharmacist_name',  'gender', 'email', 'date_of_birth', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            print(field)
        self.fields["pharmacist_name"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["gender"].widget.attrs.update({"class": 'form-control'})
        self.fields["email"].widget.attrs.update({"class": 'form-control', "type": 'email'})
        self.fields["date_of_birth"].widget.attrs.update({"class": 'form-control', "type": 'date'})
        self.fields["phone_number"].widget.attrs.update({"class": 'form-control', "type": 'text'})

class BedCategoryForm(forms.ModelForm):
    class Meta:
        model = BedCategory
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            print(field)
            new_data = {
                "label": '',
                
                "class": 'form-control'

            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )

class AddBedForm(forms.ModelForm):
    
    class Meta:
        model = AddBed
        fields = ['bedCategory_name', 'bed_number', 'charges', 'tax']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            print(field)
        self.fields["bedCategory_name"].widget.attrs.update({"class": 'form-control'})
        self.fields["bed_number"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["charges"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["tax"].widget.attrs.update({"class": 'form-control'})