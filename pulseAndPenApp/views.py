from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def sign_in(request):
    return render(request, 'signin.html')

def sign_up(request):
    return render(request, 'signup.html')

def sign_up_form(request):
    return render(request, 'signupform.html')

def privacy_policy(request):
    return render(request, 'privacyPolicy.html')

def terms_and_conditions(request):
    return render(request, 'terms.html')