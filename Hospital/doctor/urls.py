from django.urls import path
from . import views

urlpatterns = [
    path("", views.doctor_index, name="Dindex"),
    path("department/", views.doctor_department, name="department"),
    path("doctor/", views.doctor_add, name="doctor"),
    path("doctorlist/", views.doctor_list, name="doctor_list"),
]
