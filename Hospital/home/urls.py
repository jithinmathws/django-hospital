from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="Index"),
    path("home/", views.home, name="Home"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("edit/", views.editProfile, name="Edit"),
    path("changepassword/", views.change_password, name="changePassword"),
    path("changeprofile/", views.change_details, name="changeProfile"),
    path("delete_account/", views.delete_account, name="delete_account"),
    path("signout/", views.signout, name="signout"),
]
