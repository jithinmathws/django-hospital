from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="Index"),
    path("home/", views.home, name="Home"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("changepassword/", views.change_password, name="change_password"),
    
]
