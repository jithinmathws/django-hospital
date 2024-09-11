from django import forms
from django.forms.models import inlineformset_factory

import django.forms.utils
import django.forms.widgets

from .models import DoctorDepartment, DoctorInfo, PatientDetails, GuardianDetails, NurseDetails, PharmacistDetails, BedCategory, AddBed, PatientStatus, AdmissionDetails, InvoiceDetail, AppointmentDetails, TreatmentDetails, IncomeDetails, InvoiceRelation

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = DoctorDepartment
        fields = ['department_name']

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
    image = forms.ImageField(required=False)
    class Meta:
        model = DoctorInfo
        #fields = ['doctor_name', 'department_name', 'specialization', 'date_of_birth', 'gender', 'address_line', 'state', 'country', 'pin_code', 'email', 'phone_number', 'visiting_charge', 'visiting_charge_tax', 'consulting_charge', 'consulting_charge_tax', 'cv_file', 'image']
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            print(field)
        self.fields["doctor_name"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["department_name"].widget.attrs.update({"class": 'form-control'})
        self.fields["specialization"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["date_of_birth"].widget.attrs.update({"class": 'form-control', "type": 'date'})
        self.fields["gender"].widget.attrs.update({"class": 'form-control'})
        self.fields["address_line"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["state"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["country"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["pin_code"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["email"].widget.attrs.update({"class": 'form-control', "type": 'email'})
        self.fields["phone_number"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["visiting_charge"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["visiting_charge_tax"].widget.attrs.update({"class": 'form-control'})
        self.fields["consulting_charge"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["consulting_charge_tax"].widget.attrs.update({"class": 'form-control'})
        self.fields["cv_file"].widget.attrs.update({"class": 'form-control', "type": 'file'})
        #self.fields["doctor_image"].widget.attrs.update({"class": 'form-control', "type": 'file'})
        self.fields["image"].widget.attrs.update({"class": 'form-control', "type": 'file'})
            

class PatientForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={"type": 'date'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"type": 'email'}))
    patient_image = forms.ImageField(required=False)
    class Meta:
        model = PatientDetails
        #fields = ['patient_name',  'gender', 'email', 'date_of_birth', 'phone_number']
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            print(field)
        self.fields["patient_name"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["gender"].widget.attrs.update({"class": 'form-control'})
        self.fields["blood_group"].widget.attrs.update({"class": 'form-control'})
        self.fields["address"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["state"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["country"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["pin_code"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["email"].widget.attrs.update({"class": 'form-control', "type": 'email'})
        self.fields["date_of_birth"].widget.attrs.update({"class": 'form-control', "type": 'date'})
        self.fields["phone_number"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["patient_image"].widget.attrs.update({"class": 'form-control', "type": 'file'})

class PatientStatusForm(forms.ModelForm):
    class Meta:
        model = PatientStatus
        fields = ['patient_status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            print(field)
        self.fields["patient_status"].widget.attrs.update({"class": 'form-control', "type": 'text'})

class AdmissionForm(forms.ModelForm):
    admission_date = forms.DateTimeField(widget=forms.DateInput(attrs={"type": 'datetime-local'}))
    
    class Meta:
        model = AdmissionDetails
        fields = ['admission_date', 'patient_status', 'doctor_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["admission_date"].widget.attrs.update({"class": 'form-control', "type": 'datetime-local'})
        self.fields["patient_status"].widget.attrs.update({"class": 'form-control'})
        self.fields["doctor_name"].widget.attrs.update({"class": 'form-control'})

class AppointmentForm(forms.ModelForm):
    booking_date = forms.DateTimeField(widget=forms.DateInput(attrs={"type": 'datetime-local'}))
    
    class Meta:
        model = AppointmentDetails
        fields = ['patient_name', 'department_name', 'doctor_name', 'booking_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["patient_name"].widget.attrs.update({"class": 'form-control'})
        self.fields["department_name"].widget.attrs.update({"class": 'form-control'})
        self.fields["doctor_name"].widget.attrs.update({"class": 'form-control'})
        self.fields["booking_date"].widget.attrs.update({"class": 'form-control', "type": 'datetime-local'})
        

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
    nurse_image = forms.ImageField(required=False)
    class Meta:
        model = NurseDetails
        #fields = ['nurse_name',  'gender', 'email', 'date_of_birth', 'phone_number']
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            print(field)
        self.fields["nurse_name"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["department_name"].widget.attrs.update({"class": 'form-control'})
        self.fields["gender"].widget.attrs.update({"class": 'form-control'})
        self.fields["address"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["state"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["country"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["pin_code"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["salary"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["salary_tax"].widget.attrs.update({"class": 'form-control'})
        self.fields["email"].widget.attrs.update({"class": 'form-control', "type": 'email'})
        self.fields["date_of_birth"].widget.attrs.update({"class": 'form-control', "type": 'date'})
        self.fields["phone_number"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["nurse_image"].widget.attrs.update({"class": 'form-control', "type": 'file'})

class PharmacistForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={"type": 'date'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"type": 'email'}))
    pharmacist_image = forms.ImageField(required=False)
    class Meta:
        model = PharmacistDetails
        #fields = ['pharmacist_name',  'gender', 'email', 'date_of_birth', 'phone_number']
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            print(field)
        self.fields["pharmacist_name"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["gender"].widget.attrs.update({"class": 'form-control'})
        self.fields["address"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["state"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["country"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["pin_code"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["email"].widget.attrs.update({"class": 'form-control', "type": 'email'})
        self.fields["date_of_birth"].widget.attrs.update({"class": 'form-control', "type": 'date'})
        self.fields["phone_number"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["charges"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["charges_tax"].widget.attrs.update({"class": 'form-control'})
        self.fields["pharmacist_image"].widget.attrs.update({"class": 'form-control', "type": 'file'})
        

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

    def clean_bed_category(self):
        bed_category = self.cleaned_data.get('bedCategory_name')
        if not bed_category:
            raise forms.ValidationError('Bed Category required')
        return bed_category
    
    def clean_bed_number(self):
        bed_number = self.cleaned_data.get('bed_number')
        if not bed_number:
            raise forms.ValidationError('Bed Number required')
        for instance in AddBed.objects.all():
            if instance.bed_number == bed_number:
                raise forms.ValidationError('Bed already exist')
        return bed_number

class InvoiceRelationForm(forms.ModelForm):
        
    class Meta:
        model = InvoiceRelation
        #fields = ['invoice_title', 'subtotal_amount']
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            print(field)
        self.fields["invoice_title"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["subtotal_amount"].widget.attrs.update({"class": 'form-control', "type": 'text', "onkeyup": 'subcalc(this)'})

class InvoiceForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={"type": 'date'}))
    
    class Meta:
        model = InvoiceDetail
        #fields = ['patient_name', 'invoice_title', 'subtotal_amount', 'discount_amount', 'discount_percentage', 'tax_percentage', 'tax_amount', 'adjusted_amount', 'date']
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            print(field)
        #self.fields["invoice_id"].widget.attrs.update({"class": 'form-control'})
        self.fields["patient_name"].widget.attrs.update({"class": 'form-control'})
        
        self.fields["total_amount"].widget.attrs.update({"class": 'form-control', "type": 'number', "onkeyup": 'totalcalc(this)'})
        self.fields["discount_amount"].widget.attrs.update({"class": 'form-control', "type": 'number', "onkeyup": 'discountcalc(this)', "value": 0 })
        self.fields["discount_percentage"].widget.attrs.update({"class": 'form-control', "onkeyup": 'percentagecalc(this)', "type": 'number', "value": 0})
        self.fields["tax_amount"].widget.attrs.update({"class": 'form-control', "type": 'number', "onkeyup": 'discountcalc(this)', "value": 0 })
        self.fields["tax_percentage"].widget.attrs.update({"class": 'form-control', "type": 'number', "value": 0, "onkeyup": 'percentagecalc(this)'})
        self.fields["adjusted_amount"].widget.attrs.update({"class": 'form-control', "type": 'number'})
        self.fields["date"].widget.attrs.update({"class": 'form-control', "type": 'date'})

InvoiceFormSet = inlineformset_factory(
    InvoiceDetail,
    InvoiceRelation,
    InvoiceRelationForm,
    min_num=1,
    extra=0
)

class IncomeForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={"type": 'date'}))
    
    class Meta:
        model = IncomeDetails
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            print(field)
        self.fields["patient_name"].widget.attrs.update({"class": 'form-control'})
        self.fields["payment_status"].widget.attrs.update({"class": 'form-control'})
        self.fields["payment_method"].widget.attrs.update({"class": 'form-control'})
        self.fields["payment_details"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["date"].widget.attrs.update({"class": 'form-control', "type": 'date'})
        self.fields["payment_amount"].widget.attrs.update({"class": 'form-control', "type": 'text'})

class TreatmentForm(forms.ModelForm):
    class Meta:
        model = TreatmentDetails
        fields = ['treatment_name',  'treatment_price', 'tax']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            print(field)
        self.fields["treatment_name"].widget.attrs.update({"class": 'form-control', "type": 'text'})
        self.fields["treatment_price"].widget.attrs.update({"class": 'form-control', "type": 'text'}) 
        self.fields["tax"].widget.attrs.update({"class": 'form-control'})
              