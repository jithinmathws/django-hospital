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
    path("roles/", views.roles, name="roles"),
    path("rolelist/", views.rolelist, name="rolelist"),
    path("createrole/", views.create_role, name="createrole"),
    path("edit_role-account/<int:role_id>/", views.edit_role, name="edit_role"),
    path("delete_role-account/<int:role_id>/", views.delete_role, name="delete_role"),
    
    path("staff/", views.staff, name="staff"),
    path("staff_list/", views.staff_list, name="staff_list"),
    path("createstaff/", views.create_staff_employee, name="createstaff"),
    path("edit_staff-account/<int:user_id>/", views.edit_staff_employee, name="edit_staff"),
    path("delete_staff-account/<int:user_id>/", views.delete_staff_employee, name="delete_staff"),

]
