from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from rest_framework.parsers import JSONParser
import io
from datetime import datetime
from .serializers import UserSerializer, LoginSerializer, ContactSerializer


# Render static pages
def index(request):
    return render(request, 'index.html')


def user_home(request):
    return render(request, 'userhome.html')


def forgot_password(request):
    return render(request, 'forgotpassword.html')


def sign_in(request):
    return render(request, 'signin.html')


def sign_up(request):
    return render(request, 'signup.html')

def sign_up_form(request):
    return render(request, 'signupform.html')


def contact(request):
    return render(request, 'contact.html')


def about(request):
    return render(request, 'about.html')


def privacy_policy(request):
    return render(request, 'privacyPolicy.html')


def terms_and_conditions(request):
    return render(request, 'terms.html')


# API Views for handling form submissions
class SignInView(APIView):
    def post(self, request):
        data = request.data
        data['date_time'] = datetime.now()
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"submitted": "true"}, status=status.HTTP_201_CREATED)
        return Response({"submitted": "false", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class SignUpView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"submitted": "true"}, status=status.HTTP_201_CREATED)
        return Response({"submitted": "false", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ContactView(APIView):
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Contact form submitted successfully!", "status": "success"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
