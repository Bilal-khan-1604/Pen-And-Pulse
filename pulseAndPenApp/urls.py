from django.urls import path
from pulseAndPenApp import views

urlpatterns = [
    path('', views.index, name='home'),
    path('sign-in', views.sign_in, name='signIn'),
    path('sign-up', views.sign_up, name='sign-up'),
    path('sign-up-form', views.sign_up_form, name='sign-up-form'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-and-conditions/', views.terms_and_conditions, name='terms_and_conditions'),
]
