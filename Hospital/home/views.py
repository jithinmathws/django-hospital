from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth import login, logout, authenticate
from home.forms import SignUpForm, LoginForm, ChangePasswordForm, ChangeProfileForm, RoleForm, CreateStaffEmployeeForm, EditStaffEmployeeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, User, Permission
from django.contrib import messages
from functools import wraps

# Create your views here.
def index(request):
    return render(request, "home/index.html", {})


def signup(request):
    #form = UserCreationForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            login(request, user)
            return redirect('login')
    
    else:
        form = SignUpForm()
    return render(request, 'home/signup.html', {'form' : form})

@login_required
def home(request):
    return render(request, "home/home.html", {})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect('Home')

    else:
        form = LoginForm()
    return render(request, 'home/login.html', {'form':form})

@login_required
def change_password(request):
    form = ChangePasswordForm(request.user)
    return render(request, "home/change_password.html", {'form': form})

@login_required
def editProfile(request):
    return render(request, "home/edit_profile.html", {})

@login_required
def change_details(request):

    if request.method == 'POST':
        form = ChangeProfileForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            return redirect('Home')

    else:
        #form = UserChangeForm(instance=request.user)
        form = ChangeProfileForm(instance=request.user)
    return render(request, "home/change_profile.html", {'form': form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('login')
    return render(request, "home/delete_account.html", {})

@login_required
def signout(request):
    logout(request)
    return redirect('login')

def user_has_role_or_superuser(roles):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            user_groups = request.user.groups.all().values_list('name', flat=True)

            if request.user.is_superuser or any(role in user_groups for role in roles):
                return view_func(request, *args, **kwargs)
            else:
                return redirect('Home')
        return _wrapped_view
    return decorator

def is_superuser(user):
    return user.is_superuser

@login_required
@user_has_role_or_superuser(['Administration'])
def roles(request):
    return render(request, "home/roles_index.html", {})

@login_required
@user_passes_test(is_superuser)
def rolelist(request):
    roles = Group.objects.all()
    return render(request, "home/role_list.html", {'roles': roles})

@login_required
@user_passes_test(is_superuser)
def create_role(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff')
    else:
        form = RoleForm()
    return render(request, "home/create_role.html", {'form': form})

@login_required
@user_passes_test(is_superuser)
def edit_role(request, role_id):
    role = Group.objects.get(pk=role_id)
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            role = form.save()
            return redirect('rolelist')

    else:
        form = RoleForm(instance=role)
    return render(request, 'home/edit_role.html', {'form': form, 'role': role})


@login_required
@user_passes_test(is_superuser)
def delete_role(request, role_id):
    role = Group.objects.get(pk=role_id)

    GroupUsers = User.objects.filter(groups_name=role).count()

    if(GroupUsers == 0):
        role.delete()
        return redirect('rolelist')
    else:
        ErrorMessage = "This Role cannot be deleted, as it has users"
        return HttpResponse(ErrorMessage)
    

@login_required
@user_passes_test(is_superuser)
def staff(request):
    return render(request, "home/staff_index.html", {})

@login_required
#@user_passes_test(is_superuser)
@user_has_role_or_superuser(['HR', 'SeniorHR', 'Director'])
def staff_list(request):
    staff_members = User.objects.filter(is_staff=True)
    user_groups = request.user.groups.all().values_list('name', flat=True)
    return render(request, "home/staff_list.html", {'staff_members': staff_members, 'user': request.user, 'user_groups': user_groups})

@login_required
#@user_passes_test(is_superuser)
@user_has_role_or_superuser(['HR'])
def create_staff_employee(request):

    if request.method  == 'POST':
        form = CreateStaffEmployeeForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()

            rolename = form.cleaned_data.get('role')
            staff_group, created = Group.objects.get_or_create(name=rolename)
            user.groups.add(staff_group)

            return redirect('staff')
    else:
        form = CreateStaffEmployeeForm()
    return render(request, "home/create_staff_employee.html", {'form': form})

@login_required
#@user_passes_test(is_superuser)
@user_has_role_or_superuser(['SeniorHR'])
def edit_staff_employee(request, user_id):
    staff_member = User.objects.get(pk=user_id)

    if request.method == 'POST':
        form = EditStaffEmployeeForm(request.POST, instance=staff_member)
        if form.is_valid():
            user = form.save()

            rolename = form.cleaned_data.get('role')
            staff_group, created = Group.objects.get_or_create(name=rolename)
            user.groups.clear()
            user.groups.add(staff_group)

            return redirect('staff_list')
    
    else:
        groupname = staff_member.groups.values_list('name', flat=True).first()
        staff_group = Group.objects.get(name=groupname)
        form = EditStaffEmployeeForm(instance=staff_member)
    return render(request, "home/edit_staff.html", {'form': form, 'staff_member': staff_member, 'staff_group': staff_group})


@login_required
#@user_passes_test(is_superuser)
@user_has_role_or_superuser(['Director'])
def delete_staff_employee(request, user_id):
    staff_member = User.objects.get(pk=user_id)
    staff_member.delete()
    return redirect('staff_list')    

@login_required
@user_passes_test(is_superuser)
def associate_permissions(request, role_id):
    role = Group.objects.get(pk=role_id)
    relevant_permissions = ['view_staffuser', 'change_staffuser', 'delete_staffuser', 'add_staffuser',]

    if request.method == 'POST':
        try:
            selected_permission_ids = request.POST.getlist('permissions')
            selected_permissions = Permission.objects.filter(pk__in=selected_permission_ids)

            role.permissions.set(selected_permissions)

            messages.success(request, "Permissions associated successfully!")
            return redirect('role_list')
        
        except Exception as e:
            print(f"Error associating permissions: {e}")
            messages.error(request, "An error occured while associating permissions. Please try again!")

    else:    
        all_permissions = Permission.objects.filter(codename__in=relevant_permissions)
    
    return render(request, 'home/associate_permissions.html', {'role': role, 'all_permissions': all_permissions})


