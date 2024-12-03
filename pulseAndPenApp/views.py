from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def privacy_policy(request):
    return render(request, 'privacyPolicy.html')