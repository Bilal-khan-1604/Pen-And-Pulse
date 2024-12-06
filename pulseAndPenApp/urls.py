from django.urls import path
from pulseAndPenApp import views

urlpatterns = [
    path('', views.index, name='home'),
    path('sign-in', views.sign_in, name='sign-in'),
    path('forgot-password', views.forgot_password, name='forgot-password'),
    path('sign-up', views.sign_up, name='sign-up'),
    path('sign-up-form', views.sign_up_form, name='sign-up-form'),
    path('user-home', views.user_home, name='user-home'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('privacy-policy', views.privacy_policy, name='privacy-policy'),
    path('terms-and-conditions', views.terms_and_conditions, name='terms-and-conditions'),
    path('signin/authenticate', views.SignInView.as_view(), name='signin_api'),
    path('signup/register', views.SignUpView.as_view(), name='signup_api'),
    path('contact/form/submit', views.ContactView.as_view(), name='contact_api'),
]
