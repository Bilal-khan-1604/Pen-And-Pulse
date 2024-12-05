from django.shortcuts import render
from pulseAndPenApp.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, 'index.html')

def sign_in(request):
    return render(request, 'signin.html')

def sign_up(request):
    return render(request, 'signup.html')

def sign_up_form(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        new_user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        new_user.save()

    return render(request, 'signupform.html')

def privacy_policy(request):
    return render(request, 'privacyPolicy.html')

def terms_and_conditions(request):
    return render(request, 'terms.html')