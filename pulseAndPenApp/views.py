from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from .serializers import UserSerializer, ContactSerializer, BlogSerializer
from datetime import datetime, timezone, timedelta
from functools import wraps
import jwt, cloudinary, cloudinary.uploader

def auth_required(optional=False):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            token = request.COOKIES.get('authToken')

            if not token:
                if optional:
                    return view_func(request, *args, **kwargs)
                return redirect('/login/')

            try:
                payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
                request.user_id = payload.get("id")
                return view_func(request, *args, **kwargs)
            except jwt.ExpiredSignatureError:
                response = redirect('/login/')
                response.delete_cookie('authToken')
                return response
            except jwt.InvalidTokenError:
                response = redirect('/login/')
                response.delete_cookie('authToken')
                return response

        return wrapper
    return decorator


def index(request):
    return render(request, 'pulseAndPenApp/index.html')


def forgot_password(request):
    return render(request, 'pulseAndPenApp/forgotpassword.html')


def join(request):
    return render(request, 'pulseAndPenApp/joinnow.html')


def about(request):
    return render(request, 'pulseAndPenApp/about.html')


def privacy_policy(request):
    return render(request, 'pulseAndPenApp/privacyPolicy.html')


def terms_and_conditions(request):
    return render(request, 'pulseAndPenApp/terms.html')


@auth_required(optional=True)
def home_view(request):
    return render(request, 'pulseAndPenApp/home.html')


@auth_required()
def publish(request):
    return render(request, 'pulseAndPenApp/publish.html')


class LoginView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'registration/login.html')

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, username=email, password=password)

        if user:
            payload = {
                'id': user.id,
                'email': user.email,
                'exp': datetime.now(timezone.utc) + timedelta(seconds=settings.JWT_EXPIRATION_TIME)
            }
            token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

            response = redirect('home')
            response.set_cookie(
                'authToken', 
                token, 
                httponly=True,
                secure=True,
                samesite='Strict'
            )
            return response

        return Response({"error": "Incorrect email or password."}, status=status.HTTP_401_UNAUTHORIZED)


class SignupView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'registration/signup.html')

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    

class BlogCreateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        data = request.data

        thumbnail = request.FILES.get('thumbnail')
        if thumbnail:
            try:

                cloudinary.config( 
                    cloud_name = settings.CLOUDINARY_STORAGE['CLOUD_NAME'], 
                    api_key = settings.CLOUDINARY_STORAGE['API_KEY'], 
                    api_secret = settings.CLOUDINARY_STORAGE['API_SECRET'],
                    secure=True
                )

                upload_result = cloudinary.uploader.upload(thumbnail)
                data['thumbnail_url'] = upload_result['secure_url']

            except Exception as e:
                return Response({"error": "Image upload failed."}, status=400)

        serializer = BlogSerializer(data=data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
