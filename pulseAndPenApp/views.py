from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from .serializers import UserSerializer, ContactSerializer, BlogSerializer, CommentSerializer, NewsletterSubscriptionSerializer
from datetime import datetime, timezone, timedelta
from functools import wraps
import jwt, cloudinary, cloudinary.uploader
from .models import Blog, User, Comment
from django.utils.decorators import method_decorator
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import get_object_or_404
from urllib.parse import unquote
from django.http import HttpResponse

def auth_required(optional=False):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if len(args) > 0 and hasattr(args[0], 'request') and not isinstance(args[0], WSGIRequest):
                request = args[0].request
            elif len(args) > 0 and isinstance(args[0], WSGIRequest):
                request = args[0]
                
            token = request.COOKIES.get('authToken')
            request.user = False

            if token:
                try:
                    payload = jwt.decode(
                        token, 
                        settings.JWT_SECRET_KEY, 
                        algorithms=[settings.JWT_ALGORITHM]
                    )
                    request.user = User.objects.get(id=payload.get("id"))
                except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
                    if not optional:
                        response = redirect('/login/')
                        response.delete_cookie('authToken')
                        return response

            if not optional and not request.user:
                return redirect('/login/')
            
            return view_func(request, *args, **kwargs)
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
    return render(request, 'pulseAndPenApp/home.html', {
        'authenticatedUser': bool(request.user),
        'user_info': request.user
    })


@auth_required(optional=True)
def blogs(request, type):
    print(type)
    blog_list = Blog.objects.filter(category=type)
    print(blog_list)

    paginator = Paginator(blog_list, 5)
    page = request.GET.get('page')

    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)

    context = {
        'type': type,
        'blogs': blogs,
        'authenticatedUser': bool(request.user),
        'user_info': request.user
    }

    return render(request, 'pulseAndPenApp/blogs.html', context)


@auth_required(optional=True)
def complete_blog(request, title):
    blog = get_object_or_404(Blog, title=unquote(title))
    context = {
        'blog': blog,
        'authenticatedUser': bool(request.user),
        'user_info': request.user
    }

    return render(request, 'pulseAndPenApp/complete_blog.html', context)

@auth_required()
def publish(request):
    return render(request, 'pulseAndPenApp/publish.html', {
        'authenticatedUser': bool(request.user),
        'user_info': request.user
    })


class NewsletterSubscriptionView(APIView):
    def post(self, request):
        serializer = NewsletterSubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Thank you for subscribing to our newsletter!"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def get_blog_comments(request, title, blog_id):
    blog = Blog.objects.filter(id=blog_id).first()
    if not blog:
        return HttpResponse("Blog not found", status=404)

    comments = blog.comments.select_related('user')
    comment_data = [
        {
            'text': comment.text,
            'created_at': comment.created_at,
            'user_email': comment.user.email,
            'user_id': comment.user.id,
        }
        for comment in comments
    ]

    return render(request, 'pulseAndPenApp/comments.html', {
        'comments': comment_data,
        'blog': blog,
    }) 

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
                httponly=False,
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
    

@method_decorator(auth_required(), name='post')
class BlogCreateView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request, *args, **kwargs):
        if not request.user:
            return Response({"error": "Authentication required."}, status=401)
        data = request.data
        print(data)

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
    

@method_decorator(auth_required(), name='dispatch')
class CommentView(APIView):

    def post(self, request):
        blog_id = request.data.get("blog_id")
        if not blog_id:
            return Response({"error": "Blog ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        blog = Blog.objects.filter(id=blog_id).first()
        if not blog:
            return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(blog=blog, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

