from django.utils.text import slugify

import uuid

#Unique slug for Bed Category
def generate_bed_slug(bedCategory_name:str) -> str:
    from .models import BedCategory
    bedCategory_name = slugify(bedCategory_name)
   
    while(BedCategory.objects.filter(slug = bedCategory_name).exists()):
        bedCategory_name = f'{slugify(bedCategory_name)} - {str(uuid.uuid4())[0:4]}'

    return bedCategory_name

#Unique slug for Hospital Service
def generate_service_slug(service_name:str) -> str:
    from .models import HospitalService
    service_name = slugify(service_name)
    
    while(HospitalService.objects.filter(slug = service_name).exists()):
        service_name = f'{slugify(service_name)} - {str(uuid.uuid4())[0:4]}'

    return service_name
    
#Unique slug for Stock
def generate_stock_slug(item_name:str) -> str:
    from .models import Stock
    item_name = slugify(item_name)
    
    while(Stock.objects.filter(slug = item_name).exists()):
        item_name = f'{slugify(item_name)} - {str(uuid.uuid4())[0:4]}'

    return item_name

#Unique slug for Customer
def generate_customer_slug(name:str) -> str:
    from .models import Customer
    name = slugify(name)
    
    while(Customer.objects.filter(slug = name).exists()):
        name = f'{slugify(name)} - {str(uuid.uuid4())[0:4]}'

    return name

#Unique slug for Invoice
def generate_invoice_slug(patient_name:str) -> str:
    from .models import InvoiceData
    patient_name = slugify(patient_name)
    
    while(InvoiceData.objects.filter(slug = patient_name).exists()):
        patient_name = f'{slugify(patient_name)} - {str(uuid.uuid4())[0:4]}'

    return patient_name