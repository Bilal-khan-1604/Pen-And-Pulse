from django.urls import path
from pulseAndPenApp import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.LoginView.as_view(), name='sign-in'),
    path('forgot-password', views.forgot_password, name='forgot-password'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('join/', views.join, name='join'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('about/', views.about, name='about'),
    path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
    path('terms-and-conditions/', views.terms_and_conditions, name='terms-and-conditions'),
]
