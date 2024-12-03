from django.contrib import admin
from django.urls import path
from pulseAndPenApp import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index, name=''),
    path('privacy_policy/', views.privacyPolicy, name=''),
]
