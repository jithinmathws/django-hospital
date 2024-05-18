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

    name = models.CharField(max_length=50)
    department_name = models.ForeignKey(DoctorDepartment, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    gender = models.CharField(
         max_length=20,
         choices=(("Male", "Male"), ("Female", "Female"), ("Other", "Other")),
     )
    email = models.EmailField(default="", max_length=50)
    phone_number = models.CharField(default="", max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)