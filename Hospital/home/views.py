from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from home.forms import SignUpForm


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


def home(request):
    return render(request, "home/home.html", {})