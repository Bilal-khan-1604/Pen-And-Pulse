from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, ContactSerializer
import jwt
from datetime import datetime, timezone, timedelta
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse

def index(request):
    return render(request, 'pulseAndPenApp/index.html')

def forgot_password(request):
    return render(request, 'pulseAndPenApp/forgotpassword.html')

# def home(request):
#     return render(request, 'pulseAndPenApp/home.html')


# class LoginView(APIView):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'registration/login.html')

#     def post(self, request, *args, **kwargs):
#         email = request.data.get("email")
#         password = request.data.get("password")
#         user = authenticate(request, username=email, password=password)
#         if user:
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({"token": token.key}, status=status.HTTP_200_OK)
#         return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class LoginView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'registration/login.html')

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, username=email, password=password)

        if user:
            # Generate JWT Token
            payload = {
                'id': user.id,
                'email': user.email,
                'exp': datetime.now(timezone.utc) + timedelta(seconds=settings.JWT_EXPIRATION_TIME)
            }
            token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

            # Redirect to the user home page with the token set in a cookie
            response = redirect('home')  # Replace 'user_home' with your home view's name or URL
            response.set_cookie(
                'authToken', 
                token, 
                httponly=True,    # Secure against XSS
                secure=True,      # Use True in production with HTTPS
                samesite='Strict' # Prevent CSRF attacks
            )
            return response

        return Response({"error": "Incorrect email or password."}, status=status.HTTP_401_UNAUTHORIZED)


class HomeView(APIView):
    def get(self, request, *args, **kwargs):
        # Extract JWT token from the cookie
        token = request.COOKIES.get('authToken')
        if not token:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Decode JWT token
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            user_id = payload.get("id")
            # Fetch user information or render the home page
            return render(request, 'pulseAndPenApp/userhome.html', {"user_id": user_id})
        except jwt.ExpiredSignatureError:
            return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)


class SignupView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'registration/signup.html')

    def post(self, request, *args, **kwargs):
        # Handle form submission
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def join(request):
    return render(request, 'pulseAndPenApp/joinnow.html')


def about(request):
    return render(request, 'pulseAndPenApp/about.html')


def privacy_policy(request):
    return render(request, 'pulseAndPenApp/privacyPolicy.html')


def terms_and_conditions(request):
    return render(request, 'pulseAndPenApp/terms.html')

class ContactView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'pulseAndPenApp/contact.html')
    
    def post(self, request, *args, **kwargs):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Contact form submitted successfully!", "status": "success"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
