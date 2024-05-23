from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

# Create your models here.

class CustomPermission(models.Model):
    permission = models.OneToOneField(Permission, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.permission.name
    
    class Meta:
        permissions = (
            ("add_staffuser", "Can add Staff users"),
            ("change_staffuser", "Can edit Staff users"),
            ("view_staffuser", "Can view Staff users"),
            ("delete_staffuser", "Can delete Staff users"),
        )
