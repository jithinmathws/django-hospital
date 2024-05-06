from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth import login, logout, authenticate
from home.forms import SignUpForm, LoginForm, ChangePasswordForm, ChangeProfileForm
from django.contrib.auth.decorators import login_required

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