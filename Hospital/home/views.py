from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from home.forms import SignUpForm, LoginForm
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
            return redirect('Home')
    
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