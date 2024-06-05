from django.db import models
from django.utils.text import slugify

# Create your models here.
class DoctorDepartment(models.Model):
    department_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.department_name)

    def save(self, *args, **kwargs):
        if not self.slug:
            # generate slug
            self.slug = slugify(self.department_name)
        super().save(*args, **kwargs)


class DoctorDetails(models.Model):

    doctor_name = models.CharField(max_length=50)
    department_name = models.ForeignKey(DoctorDepartment, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    gender = models.CharField(
         max_length=20,
         choices=(("Male", "Male"), ("Female", "Female"), ("Other", "Other")),
     )
    email = models.EmailField(default="", max_length=50, unique=True)
    phone_number = models.CharField(default="", max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.doctor_name)
    
class PatientDetails(models.Model):
    patient_name = models.CharField(max_length=50)
    gender = models.CharField(
         max_length=20,
         choices=(("Male", "Male"), ("Female", "Female"), ("Other", "Other")),
     )
    email = models.EmailField(default="", max_length=50, unique=True)
    date_of_birth = models.DateField()
    phone_number = models.CharField(default="", max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.patient_name)
    
class PatientStatus(models.Model):
    patient_status = models.CharField(max_length=50)

    def __str__(self):
        return str(self.patient_status)
    
class AdmissionDetails(models.Model):
    admission_date = models.DateTimeField(null=True, blank=True)
    patient_status = models.ForeignKey(PatientStatus, on_delete=models.CASCADE)
    doctor_name = models.ForeignKey(DoctorDetails, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.doctor_name)

class AppointmentDetails(models.Model):
    patient_name = models.ForeignKey(PatientDetails, on_delete=models.CASCADE)
    department_name = models.ForeignKey(DoctorDepartment, on_delete=models.CASCADE)
    doctor_name = models.ForeignKey(DoctorDetails, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.doctor_name)
    
class GuardianDetails(models.Model):

    guardian_name = models.CharField(max_length=50)
    patient_name = models.ForeignKey(PatientDetails, on_delete=models.CASCADE)
    
    gender = models.CharField(
         max_length=20,
         choices=(("Male", "Male"), ("Female", "Female"), ("Other", "Other")),
     )
    email = models.EmailField(default="", max_length=50, unique=True)
    date_of_birth = models.DateField()
    phone_number = models.CharField(default="", max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.guardian_name)
    
class NurseDetails(models.Model):

    nurse_name = models.CharField(max_length=50)
    gender = models.CharField(
         max_length=20,
         choices=(("Male", "Male"), ("Female", "Female"), ("Other", "Other")),
     )
    email = models.EmailField(default="", max_length=50, unique=True)
    date_of_birth = models.DateField()
    phone_number = models.CharField(default="", max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.nurse_name)
    
class PharmacistDetails(models.Model):

    pharmacist_name = models.CharField(max_length=50)
    gender = models.CharField(
         max_length=20,
         choices=(("Male", "Male"), ("Female", "Female"), ("Other", "Other")),
     )
    email = models.EmailField(default="", max_length=50, unique=True)
    date_of_birth = models.DateField()
    phone_number = models.CharField(default="", max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pharmacist_name)
    
class BedCategory(models.Model):
    bedCategory_name = models.CharField(max_length=200, unique=True)
    #slug = models.SlugField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.bedCategory_name)

class AddBed(models.Model):
    bedCategory_name = models.ForeignKey(BedCategory, on_delete=models.CASCADE)
    bed_number = models.CharField(max_length=50)
    charges = models.CharField(max_length=50)
    tax = models.CharField(
         max_length=20,
         choices=(("10%", "10%"), ("15%", "15%"), ("20%", "20%")),
     )

    def __str__(self):
        return str(self.bed_number)
    
class InvoiceDetails(models.Model):
    invoice_id = models.BigAutoField(primary_key=True)
    patient_name = models.ForeignKey(PatientDetails, on_delete=models.CASCADE)
    invoice_title = models.CharField(max_length=50)
    subtotal_amount = models.CharField(max_length=50)
    adjusted_amount = models.CharField(max_length=50)
    date = models.DateField()

    def __str__(self):
        return str(self.invoice_title)
    
class TreatmentDetails(models.Model):
    treatment_name = models.CharField(max_length=50)
    treatment_price = models.CharField(max_length=50)
    tax = models.CharField(
         max_length=20,
         choices=(("5%", "5%"), ("10%", "10%"), ("15%", "15%")),
     )