from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.db.models import Case, When

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator

from django.db.models import Max, Value
from django.utils.text import slugify
from .utils import *

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

class DoctorInfo(models.Model):
    doctor_name = models.CharField(max_length=50)
    department_name = models.ForeignKey(DoctorDepartment, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField()
    gender = models.CharField(
         max_length=20,
         choices=(("Male", "Male"), ("Female", "Female"), ("Other", "Other")),
     )
    address_line = models.CharField(max_length=250, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    pin_code = models.BigIntegerField(blank=True, null=True)
    email = models.EmailField(default="", max_length=50, unique=True)
    phone_number = models.CharField(default="", max_length=20)
    visiting_charge = models.CharField(max_length=50, blank=True, null=True)
    visiting_charge_tax = models.CharField(
         max_length=20, blank=True, null=True,
         choices=(("10%", "10%"), ("15%", "15%"), ("20%", "20%")),
     )
    consulting_charge = models.CharField(max_length=50, blank=True, null=True)
    consulting_charge_tax = models.CharField(
         max_length=20, blank=True, null=True,
         choices=(("10%", "10%"), ("15%", "15%"), ("20%", "20%")),
     )
    cv_file = models.FileField(upload_to='doctor/cv/', null=True, blank=True)
    #certificate = models.FileField(upload_to='doctor/certificates', null=True, blank=True)
    #doctor_image = models.ImageField(upload_to='doctor/', null=True, blank=True)
    image = models.BinaryField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.doctor_name)

class CertificateDoctor(models.Model):
    doctor = models.ForeignKey(DoctorInfo, on_delete=models.CASCADE)
    certificate_file = models.FileField(upload_to='doctor/certificates/', null=True, blank=True)

    def __str__(self):
        return str(self.doctor)

class DoctorDetails(models.Model):
    doctor_name = models.CharField(max_length=50)
    department_name = models.ForeignKey(DoctorDepartment, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField()
    gender = models.CharField(
         max_length=20,
         choices=(("Male", "Male"), ("Female", "Female"), ("Other", "Other")),
     )
    address_line = models.CharField(max_length=250, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    pin_code = models.BigIntegerField(blank=True, null=True)
    email = models.EmailField(default="", max_length=50, unique=True)
    phone_number = models.CharField(default="", max_length=20)
    visiting_charge = models.CharField(max_length=50, blank=True, null=True)
    visiting_charge_tax = models.CharField(
         max_length=20, blank=True, null=True,
         choices=(("10%", "10%"), ("15%", "15%"), ("20%", "20%")),
     )
    consulting_charge = models.CharField(max_length=50, blank=True, null=True)
    consulting_charge_tax = models.CharField(
         max_length=20, blank=True, null=True,
         choices=(("10%", "10%"), ("15%", "15%"), ("20%", "20%")),
     )
    cv_file = models.FileField(upload_to='doctor/cv/', null=True, blank=True)
    certificate = models.FileField(upload_to='doctor/certificates', null=True, blank=True)
    #doctor_image = models.ImageField(upload_to='doctor/', null=True, blank=True)
    image = models.BinaryField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.doctor_name)

def certificate_path(instance, filename):
    return f'doctor/certificates/{instance.doctor.id}/{filename}'

class DoctorCertificate(models.Model):
    doctor = models.ForeignKey(DoctorDetails, on_delete=models.CASCADE)
    certificate_file = models.FileField(upload_to=certificate_path, null=True, blank=True)

    def __str__(self):
        return str(self.doctor)
'''
class PatientNumber(models.Model):
    number = models.IntegerField(null=True)

    def __str__(self):
        return str(self.number)
'''
class PatientDetails(models.Model):
    patient_number = models.IntegerField(null=True)
    patient_name = models.CharField(max_length=50)
    gender = models.CharField(
         max_length=20,
         choices=(("Male", "Male"), ("Female", "Female"), ("Other", "Other")),
     )
    blood_group = models.CharField(
        max_length=20, blank=True, null=True,
        choices=(
            ("O-", "O-"),
            ("O+", "O+"),
            ("A-", "A-"),
            ("A+", "A+"),
            ("B-", "B-"),
            ("B+", "B+"),
            ("AB-", "AB-"),
            ("AB+", "AB+"),
        ),
    )
    address = models.CharField(max_length=250, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    pin_code = models.BigIntegerField(blank=True, null=True)
    email = models.EmailField(default="", max_length=50, unique=True)
    date_of_birth = models.DateField()
    phone_number = models.CharField(default="", max_length=20)
    patient_image = models.BinaryField(blank=True, null=True)
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
    doctor_name = models.ForeignKey(DoctorInfo, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.doctor_name)

class AppointmentDetails(models.Model):
    patient_name = models.ForeignKey(PatientDetails, on_delete=models.CASCADE)
    department_name = models.ForeignKey(DoctorDepartment, on_delete=models.CASCADE)
    doctor_name = models.ForeignKey(DoctorInfo, on_delete=models.CASCADE)
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
    department_name = models.ForeignKey(DoctorDepartment, on_delete=models.CASCADE, blank=True, null=True)
    gender = models.CharField(
         max_length=20,
         choices=(("Male", "Male"), ("Female", "Female"), ("Other", "Other")),
     )
    address = models.CharField(max_length=250, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    pin_code = models.BigIntegerField(blank=True, null=True)
    email = models.EmailField(default="", max_length=50, unique=True)
    date_of_birth = models.DateField()
    phone_number = models.CharField(default="", max_length=20)
    salary = models.CharField(max_length=50, blank=True, null=True)
    salary_tax = models.CharField(
         max_length=20, blank=True, null=True,
         choices=(("10%", "10%"), ("15%", "15%"), ("20%", "20%")),
     )
    nurse_image = models.BinaryField(blank=True, null=True)
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
    address = models.CharField(max_length=250, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    pin_code = models.BigIntegerField(blank=True, null=True)
    email = models.EmailField(default="", max_length=50, unique=True)
    date_of_birth = models.DateField()
    phone_number = models.CharField(default="", max_length=20)
    charges = models.CharField(max_length=50, blank=True, null=True)
    charges_tax = models.CharField(
         max_length=20, blank=True, null=True,
         choices=(("10%", "10%"), ("15%", "15%"), ("20%", "20%")),
     )
    pharmacist_image = models.BinaryField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pharmacist_name)
    
class BedCategory(models.Model):
    bedCategory_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(blank=True)
    quantity = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.bedCategory_name)

    def save(self, *args, **kwargs):
        self.slug = generate_bed_slug(self.bedCategory_name)
        super(BedCategory, self).save(*args, **kwargs)

class AddBed(models.Model):
    patient = models.ForeignKey(PatientDetails, on_delete=models.CASCADE, null=True)
    bedCategory_name = models.ForeignKey(BedCategory, on_delete=models.CASCADE)
    bed_number = models.CharField(max_length=50)
    charges = models.CharField(max_length=50)
    tax = models.CharField(
         max_length=20,
         choices=(("10%", "10%"), ("15%", "15%"), ("20%", "20%")),
     )

    def __str__(self):
        return str(self.bed_number)

#New Invoice
class HospitalService(models.Model):
    service_name = models.CharField(max_length=100, blank=False)
    slug = models.SlugField(unique=True)
    price = models.FloatField(default=0)
    tax_percentage = models.FloatField(default=0)

    def __str__(self):
        return self.service_name
    
    def save(self, *args, **kwargs):
        self.slug = generate_service_slug(self.service_name)
        super(HospitalService, self).save(*args, **kwargs)
        
    @property
    def tax_amount(self):
        amount = self.price * (self.tax_percentage/100)
        return amount
    
    @property
    def total_price(self):
        amount = self.price + self.tax_amount
        return amount

class InvoiceData(models.Model):
    #invoice_number = models.IntegerField(null=True)
    patient = models.ForeignKey(PatientDetails, on_delete=models.CASCADE)
    service = models.ManyToManyField(HospitalService, through='InvoiceItem')
    slug = models.SlugField(unique=True)
    date = models.DateField()
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.patient.patient_name

    def save(self, *args, **kwargs):
        self.slug = generate_invoice_slug(self.patient.patient_name)
        super(InvoiceData, self).save(*args, **kwargs)

    @property
    def invoice_number(self):
        default = 1001
        if self.id == 1:
            default
        elif self.id > 1:
            default += 1
        return default
    
    @property
    def total_tax(self):
        amount=0
        for tax in self.service.all():
            amount += tax.tax_amount
        return amount
    
    @property
    def final_amount(self):
        amount=0
        for price in self.service.all():
            amount += price.total_price
        return amount

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(InvoiceData, on_delete=models.CASCADE, null=True)
    service = models.ForeignKey(HospitalService, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.service.service_name
        
#Old Invoice
class MainInvoice(models.Model):
    #invoice_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(PatientDetails, on_delete=models.CASCADE)
    date = models.DateField()
    total_amount = models.CharField(max_length=50, blank=True, null=True)
    discount_amount = models.CharField(max_length=50, blank=True, null=True)
    discount_percentage = models.CharField(max_length=50, blank=True, null=True)
    tax_percentage = models.CharField(max_length=50, blank=True, null=True)
    tax_amount = models.CharField(max_length=50, blank=True, null=True)
    adjusted_amount = models.CharField(max_length=50)
    
    def __str__(self):
        return self.total_amount


class SubInvoice(models.Model):
    invoice = models.ForeignKey(MainInvoice, on_delete=models.CASCADE, blank=True, null=True)
    invoice_title = models.CharField(max_length=50, blank=True, null=True)
    subtotal_amount = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.invoice_title


class InvoiceDetail(models.Model):
    invoice_id = models.BigAutoField(primary_key=True)
    patient_name = models.ForeignKey(PatientDetails, on_delete=models.CASCADE)
    
    total_amount = models.CharField(max_length=50, blank=True, null=True)
    discount_amount = models.CharField(max_length=50, blank=True, null=True)
    discount_percentage = models.CharField(max_length=50, blank=True, null=True)
    tax_percentage = models.CharField(max_length=50, blank=True, null=True)
    tax_amount = models.CharField(max_length=50, blank=True, null=True)
    adjusted_amount = models.CharField(max_length=50)
    date = models.DateField()
    
    def __str__(self):
        return str(self.invoice_id)
    
    # def get_absolute_url(self):
    #     return reverse('invoice_profile', kwargs={'pk', self.id})

class InvoiceRelation(models.Model):
    invoice_title = models.CharField(max_length=50, blank=True, null=True)
    subtotal_amount = models.CharField(max_length=50, blank=True, null=True)
    invoice_relate = models.ForeignKey(InvoiceDetail, related_name="invoice", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.invoice_relate.date

    class Meta:
        db_table = "invoice"
#Old invoice model ends


class IncomeDetails(models.Model):
    patient_name = models.ForeignKey(PatientDetails, on_delete=models.CASCADE)
    payment_status = models.CharField(
         max_length=20, blank=True, null=True,
         choices=(("PD", "Paid"), ("PNDG", "PENDING"), ("NPD", "Not Paid")),
     )
    payment_method = models.CharField(
         max_length=20, blank=True, null=True,
         choices=(("CSH", "Cash"), ("CRD", "Card"), ("UPI", "Upi")),
     )
    payment_details = models.CharField(max_length=50)
    date = models.DateField()
    payment_amount = models.CharField(max_length=50)

    def __str__(self):
        return self.patient_satus

class TreatmentDetails(models.Model):
    treatment_name = models.CharField(max_length=50)
    treatment_price = models.CharField(max_length=50)
    tax = models.CharField(
         max_length=20,
         choices=(("5%", "5%"), ("10%", "10%"), ("15%", "15%")),
     )

#inventory_pharmacy
class Category(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    slug = models.SlugField(max_length=200, blank=True, null=True, unique=True)
    
    def __str__(self):
        return self.name

class Stock(models.Model):
    item_name = models.CharField(max_length=200, unique=True, blank=True, null=True,)
    slug = models.SlugField(max_length=200, blank=True, null=True, unique=True)
    description = models.CharField(max_length=500, blank=True)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)
    price = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0.0)])
    stock = models.PositiveIntegerField(default=0)
    reorder_stock = models.PositiveIntegerField(default=0)
    stock_reorder_level = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.item_name
    
    def save(self, *args, **kwargs):
        self.slug = generate_stock_slug(self.item_name)
        super(Stock, self).save(*args, **kwargs)


class Customer(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, blank=True, null=True, unique=True)
    gender = models.CharField(
         max_length=20,
         choices=(("Male", "Male"), ("Female", "Female"), ("Other", "Other")),
     )
    address = models.CharField(max_length=250, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    pin_code = models.BigIntegerField(blank=True, null=True)
    date_of_birth = models.DateField()
    phone_number = models.CharField(default="", blank=True, null=True, max_length=20)
    products = models.ManyToManyField(Stock, through='CartItem')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)
    
    def save(self, *args, **kwargs):
        self.slug = generate_customer_slug(self.name)
        super(Customer, self).save(*args, **kwargs)

class CartItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Stock, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return str(self.quantity)