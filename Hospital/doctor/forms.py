from django import forms

from .models import DoctorDepartment, DoctorDetails

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
    class Meta:
        model = DoctorDetails
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