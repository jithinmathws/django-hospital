from import_export import resources
from .models import *

class doctorResources(resources.ModelResource):
    class meta:
        model = DoctorInfo