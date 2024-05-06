from django.shortcuts import render

# Create your views here.
def doctor_index(request):
    return render(request, "doctor/index.html", {})