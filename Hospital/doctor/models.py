from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.db.models import Case, When

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator
from shortuuid.django_fields import ShortUUIDField

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
    image = models.BinaryField(blank=True, null=True)
    next_avaialable_appointment_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.doctor_name)

class CertificateDoctor(models.Model):
    doctor = models.ForeignKey(DoctorInfo, on_delete=models.CASCADE)
    certificate_file = models.FileField(upload_to='doctor/certificates/', null=True, blank=True)

    def __str__(self):
        return str(self.doctor)

NOTIFICATION_TYPE = (
    ("New Appointment", "New Appointment"),
    ("Appointment Cancelled", "Appointment Cancelled"),
)


#old not required Doctor Field
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
#not required doctor model    

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

NOTIFICATION = (
    ("Appointment Scheduled", "Appointment Scheduled"),
    ("Appointment Cancelled", "Appointment Cancelled"),
)


class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    available_doctors = models.ManyToManyField(DoctorInfo, blank=True)

    def __str__(self):
        return f"{self.name} - {self.cost}"
        

class Appointment(models.Model):
    STATUS = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Pending', 'Pending'),
        ('Cancelled', 'Cancelled')
    ]
    
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    doctor = models.ForeignKey(DoctorInfo, on_delete=models.SET_NULL, null=True, blank=True, related_name="doctor_data")
    patient = models.ForeignKey(PatientDetails, on_delete=models.SET_NULL, null=True, blank=True, related_name="patient_data")
    appointment_date = models.DateTimeField(null=True, blank=True)
    issues = models.TextField(blank=True, null=True)
    symptoms = models.TextField(blank=True, null=True)
    appointment_id = ShortUUIDField(length=6, max_length=10, alphabet="1234567890")
    status = models.CharField(max_length=120, choices=STATUS)

    def __str__(self):
        return f"{self.patient.patient_name} with {self.doctor.doctor_name}"


class PatientNotification(models.Model):
    patient = models.ForeignKey(PatientDetails, on_delete=models.SET_NULL, null=True, blank=True)
    appointmet = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True, blank=True, related_name="patient_appointment_notification")
    type = models.CharField(max_length=100, choices=NOTIFICATION)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "PatientNotification"

    def __str__(self):
        return f"{self.patient.patient_name} PatientNotification"


class Notification(models.Model):
    doctor = models.ForeignKey(DoctorInfo, on_delete=models.SET_NULL, null=True, blank=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True, blank=True, related_name="doctor_appointment_notification")
    type = models.CharField(max_length=100, choices=NOTIFICATION_TYPE)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Notification"

    def __str__(self):
        return f"Dr {self.doctor.doctor_name} Notification"

class MedicalRecord(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    treatment = models.TextField()

    def __str__(self):
        return f"Medical record for {self.appointment.patient.patient_name}"
    
class LabTest(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    result = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.test_name)
    
class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    medications = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Prescription for {self.appointment.patient.patient_name}"

class Billing(models.Model):
    patient = models.ForeignKey(PatientDetails, on_delete=models.SET_NULL, null=True, blank=True,  related_name='billings')
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='billing', blank=True, null=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=120, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')])
    billing_id = ShortUUIDField(length=6, max_length=10, alphabet="1234567890")

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Billing for {self.patient.patient_name} - Total: {self.total}"




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

#Hospital new Bed
class Room(models.Model):
    ROOM_TYPES = (
        ('King', 'King'),
        ('Luxury', 'Luxury'),
        ('Normal', 'Normal'),
        ('Economic', 'Economic'),
        ('General Ward', 'General Ward'),

    )
    number = models.IntegerField(default=0, unique=True)
    slug = models.SlugField(blank=True)
    capacity = models.SmallIntegerField(default=0)
    numberOfBeds = models.SmallIntegerField(default=0)
    roomType = models.CharField(max_length=20, choices=ROOM_TYPES)
    price = models.FloatField(default=0)
    statusStartDate = models.DateField(null=True)
    statusEndDate = models.DateField(null=True)

    def __str__(self):
        return str(self.number)
    
    def save(self, *args, **kwargs):
        self.slug = generate_bed_slug(self.roomType)
        super(Room, self).save(*args, **kwargs)

class Booking(models.Model):
    roomNumber = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest = models.ForeignKey(PatientDetails, null=True, on_delete=models.CASCADE)
    dateOfReservation = models.DateField(default=timezone.now)
    startDate = models.DateField()
    endDate = models.DateField()

    def numOfDep(self):
        return Dependees.objects.filter(booking=self).count()

    def __str__(self):
        return str(self.roomNumber) + " " + str(self.guest)

class Dependees(models.Model):
    booking = models.ForeignKey(Booking,   null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def str(self):
        return str(self.booking) + " " + str(self.name)

class Refund(models.Model):
    guest = models.ForeignKey(PatientDetails,   null=True, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Booking, on_delete=models.CASCADE)
    reason = models.TextField()

    def __str__(self):
        return str(self.guest)

#Hospital old Bed   
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
#old bed ends

#Invoice
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
        for add in range(self.id):
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


class IncomeDetails(models.Model):
    #patient_name = models.ForeignKey(PatientDetails, on_delete=models.CASCADE)
    patient_name = models.ForeignKey(InvoiceData, on_delete=models.CASCADE, null=True, blank=True)
    payment_status = models.CharField(
         max_length=20, blank=True, null=True,
         choices=(("PAID", "Paid"), ("PARTIAL", "Partial Payment"), ("NOTPAID", "Not Paid")),
     )
    payment_method = models.CharField(
         max_length=20, blank=True, null=True,
         choices=(("CASH", "Cash"), ("CARD", "Card"), ("UPI", "Upi")),
     )
    payment_details = models.CharField(max_length=50)
    date = models.DateField()
    payment_amount = models.IntegerField(default=0)

    def __str__(self):
        return self.patient_satus
    
    @property
    def balance_amount(self):
        amount=0
        amount = self.patient_name.final_amount - self.payment_amount
        return amount

class PaymentDetails(models.Model):
    income = models.ForeignKey(IncomeDetails, on_delete=models.CASCADE)
    invoice = models.ForeignKey(InvoiceData, on_delete=models.CASCADE, null=True)

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