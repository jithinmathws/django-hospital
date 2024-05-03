from typing import Any
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm

class SignUpForm(UserCreationForm): 
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    #password = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

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

class LoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ['username', 'password']

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

class ChangePasswordForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ['old_password', 'password1', 'password2']

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